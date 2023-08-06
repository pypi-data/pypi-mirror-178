"""Loading data for neural decoding

## Examples

Let's build a simple dataset for neural decoding. The first step is determining
what data we'll use. Depending on where our data is stored we'll use different
classes that inherit from preconstruct.sources.DataSource. For example, if we want to
use data from a local folder on our computer we might use preconstruct.sources.FsSource.
For other options, see preconstruct.sources. In this example, we'll use
preconstruct.sources.NeurobankSource, which will automatically download a list of
identifiers from Neurobank. Let's suppose we know we want to use a pprox responses
from two files with identifiers `P120_1_1_c92` and `P120_1_1_c89`.
>>> from preconstruct.sources import NeurobankSource
>>> import asyncio
>>> responses = ['P120_1_1_c92', 'P120_1_1_c89']
>>> stimuli = [] # we'll leave this empty for now
>>> url = 'https://gracula.psyc.virginia.edu/neurobank/'
>>> test_source = asyncio.run(NeurobankSource.create(url, stimuli, responses))

We can't use this `DataSource` to build a dataset because it doesn't contain any
of the stimuli that were presented during the recording, but we can easily get
a list of the stimuli identifiers:
>>> stimuli = list(test_source.stimuli_names_from_pprox())
>>> sorted(stimuli)
['c95zqjxq', 'g29wxi4q', 'igmi8fxa', 'jkexyrd5', 'l1a3ltpy', 'mrel2o09', \
'p1mrfhop', 'vekibwgj', 'w08e1crn', 'ztqee46x']

Let's make a new DataSource that includes the stimuli
>>> data_source = asyncio.run(NeurobankSource.create(url, stimuli, responses))

Now we can start building our dataset. We will put our data into a
`DatasetBuilder`, which will allow us to configure the format of our dataset.
>>> from preconstruct.dataset import DatasetBuilder
>>> builder = DatasetBuilder()
>>> builder.set_data_source(data_source)
>>> builder.load_responses()

The first choice we have to make is how to represent the stimulus. Auditory
stimuli are converted to spectrograms with one or more frequency channels. An
important choice is the size of the time step, as this determines the
granularity of the time axis for both the spikes and the stimuli. The unit for
this argument and all other time values will be seconds. Note that due to the
discrete sampling rate of the stimulus, the actual time step may be slightly
larger or smaller than requested.
>>> from preconstruct.stimuliformats import Gammatone
>>> builder.add_stimuli(
...     Gammatone(
...         window_time=0.005,
...         frequency_bin_count=50,
...         min_frequency=500,
...         max_frequency=8000,
...         log_transform_compress=1,
...     ),
...     time_step=0.005,       # 5 ms
... )

Once the time resolution is set by the stimulus, the spike times can be binned:
>>> builder.bin_responses()

Now we will convert the binned spikes into a lagged matrix, with a with a window
of size tau.
>>> builder.create_time_lags(tau=0.3)

Our next step is to combine data from multiple presentations of the same stimulus.
(This is optional.)
>>> builder.pool_trials()

We have finished building our dataset.
We should investigate our object a bit, to make sure we understand how
it's structured.
>>> dataset = builder.get_dataset()

>>> dataset.responses.index
MultiIndex([('c95zqjxq',                1.0),
            ('c95zqjxq', 1.0050000000000001),
            ('c95zqjxq',               1.01),
            ('c95zqjxq', 1.0150000000000001),
            ('c95zqjxq',               1.02),
            ('c95zqjxq',              1.025),
            ('c95zqjxq',               1.03),
            ('c95zqjxq',              1.035),
            ('c95zqjxq',               1.04),
            ('c95zqjxq',              1.045),
            ...
            ('ztqee46x',              3.095),
            ('ztqee46x',                3.1),
            ('ztqee46x',              3.105),
            ('ztqee46x',               3.11),
            ('ztqee46x',              3.115),
            ('ztqee46x',               3.12),
            ('ztqee46x',              3.125),
            ('ztqee46x',               3.13),
            ('ztqee46x', 3.1350000000000002),
            ('ztqee46x',               3.14)],
           names=['stimulus.name', 'time'], length=4112)
>>> dataset.responses.columns
MultiIndex([('P120_1_1_c89',                 0.0),
            ('P120_1_1_c89',               0.005),
            ('P120_1_1_c89',                0.01),
            ('P120_1_1_c89',               0.015),
            ('P120_1_1_c89',                0.02),
            ('P120_1_1_c89',               0.025),
            ('P120_1_1_c89',                0.03),
            ('P120_1_1_c89',               0.035),
            ('P120_1_1_c89',                0.04),
            ('P120_1_1_c89',               0.045),
            ...
            ('P120_1_1_c92',                0.25),
            ('P120_1_1_c92',               0.255),
            ('P120_1_1_c92',                0.26),
            ('P120_1_1_c92',               0.265),
            ('P120_1_1_c92',                0.27),
            ('P120_1_1_c92',               0.275),
            ('P120_1_1_c92',                0.28),
            ('P120_1_1_c92', 0.28500000000000003),
            ('P120_1_1_c92',                0.29),
            ('P120_1_1_c92',               0.295)],
           names=['neuron', 'offset'], length=120)

Let's use our dataset to perform a simple neural decoding task

>>> from sklearn.linear_model import Ridge
>>> import numpy as np
>>> training_stimuli = ['c95zqjxq', 'g29wxi4q', 'igmi8fxa', 'jkexyrd5', 'l1a3ltpy', 'mrel2o09']
>>> test_stimuli = set(dataset.responses.index.get_level_values(level='stimulus.name')).difference(training_stimuli)
>>> X, Y = dataset[list(training_stimuli)]
>>> X.shape, Y.shape
((2476, 120), (2476, 50))
>>> model = Ridge(alpha=1.0)
>>> model.fit(X, Y)
Ridge()
>>> model.score(X, Y)
0.30159992
>>> X_test, Y_test = dataset[list(test_stimuli)]
>>> model.score(X_test, Y_test)
0.15341238

"""
from typing import List, Optional, Dict, Tuple

import numpy as np
import pandas as pd
from scipy.linalg import hankel

from preconstruct.sources import DataSource
from preconstruct.basisfunctions import Basis
from preconstruct.stimuliformats import StimuliFormat


class Dataset:
    """Holds constructed response matrix and stimuli

    [Quick guide to Pandas indexing](https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html#min-tut-03-subset)

    Note: You can index straight into a `Dataset` object to get stimuli and
    responses in numpy array format, but you must select rows rather than
    columns. This corresponds to the `df.loc[]` Pandas syntax, rather than
    `df[]`.

    <!--
    >>> import asyncio
    >>> from preconstruct.sources import NeurobankSource
    >>> from preconstruct.stimuliformats import Gammatone
    >>> responses = ['P120_1_1_c92']
    >>> url = 'https://gracula.psyc.virginia.edu/neurobank/'
    >>> stimuli = ['c95zqjxq', 'g29wxi4q', 'igmi8fxa', 'jkexyrd5', 'l1a3ltpy',
    ...         'mrel2o09', 'p1mrfhop', 'vekibwgj', 'w08e1crn', 'ztqee46x']
    >>> data_source = asyncio.run(NeurobankSource.create(url, stimuli, responses))
    >>> builder = DatasetBuilder()
    >>> builder.set_data_source(data_source)
    >>> builder.load_responses()
    >>> builder.add_stimuli(Gammatone(
    ...     window_time=0.005,
    ...     frequency_bin_count=50,
    ...     min_frequency=500,
    ...     max_frequency=8000,
    ...     log_transform_compress=1,
    ... ), time_step=0.005)
    >>> builder.bin_responses()
    >>> builder.create_time_lags(tau=0.3)

    -->
    >>> dataset = builder.get_dataset()
    >>> X, Y = dataset[20:30]
    >>> X.shape
    (4600, 60)
    >>> Y.shape
    (4600, 50)

    You can also manually select directly from the DataFrames.
    """

    responses: Optional[pd.DataFrame] = None
    """Columns correspond to pprox files
    """
    stimuli: Optional[pd.DataFrame] = None
    """"""
    trial_data: Optional[pd.DataFrame] = None
    """Each row corresponds to a trial and each column corresponds to a key in the
    pprox
    """
    time_step: Optional[float] = None
    """granularity of time"""
    stimuli_format: Optional[StimuliFormat] = None
    """format of the stimuli"""

    def _get_stimuli(self) -> pd.DataFrame:
        if self.stimuli is None:
            raise InvalidConstructionSequence("add_stimuli")
        return self.stimuli

    def _get_time_step(self) -> float:
        if self.stimuli is None:
            raise InvalidConstructionSequence("add_stimuli")
        first_bins = self.stimuli.index.to_frame(index=False).iloc[:2, 1]
        return first_bins[1] - first_bins[0]

    def _get_trial_data(self) -> pd.DataFrame:
        if self.trial_data is None:
            raise InvalidConstructionSequence("load_responses")
        return self.trial_data

    def _get_responses(self) -> pd.DataFrame:
        if self.responses is None:
            raise InvalidConstructionSequence("load_responses")
        return self.responses

    def __getitem__(self, key):
        """
        get numpy arrays representing the responses and the stimuli
        at the given pandas index range. The array dimensions are (time, neuron * lag).
        The dimensions of the stimulus will depend on the StimuliFormat chosen.
        """
        selection = (
            self._get_responses()
            .index.get_level_values(0)
            .unique()
            .to_series()
            .loc[key]
        )
        responses = self._get_responses().loc[selection].to_numpy()
        try:
            stimuli_index = self._get_trial_data().loc[selection]["stimulus.name"]
        except KeyError:
            stimuli_index = key
        stimuli = self._get_stimuli_format().to_values(
            self._get_stimuli().loc[stimuli_index]
        )
        return responses, stimuli

    def _get_stimuli_format(self) -> StimuliFormat:
        if self.stimuli_format is None:
            raise InvalidConstructionSequence("add_stimuli")
        return self.stimuli_format

    def to_steps(self, time_in_seconds):
        """Converts a time in seconds to a time in steps"""
        return int(time_in_seconds / self._get_time_step())


class DatasetBuilder:
    """Construct instances of the `Dataset` class using the [builder
    pattern](https://refactoring.guru/design-patterns/builder)
    """

    data_source: DataSource
    tau: Optional[float]
    basis: Optional[np.ndarray]

    def __init__(self):
        self._dataset = Dataset()
        self.data_source = _EmptySource()

    def set_data_source(self, data_source: DataSource):
        self.data_source = data_source

    def load_responses(self, ignore_columns: Optional[List[str]] = None):
        if ignore_columns is None:
            ignore_columns = []
        clusters = self.data_source.get_responses()
        assert len(clusters) > 0, "no clusters"
        trial_data = pd.concat(
            {
                k: pd.json_normalize(v["pprox"])
                .rename(columns={"index": "trial"})
                .set_index("trial")
                for k, v in clusters.items()
            },
            axis=1,
        )
        trial_data.columns = trial_data.columns.reorder_levels(order=[1, 0])
        self._dataset.responses = trial_data["events"].rename_axis(columns="neuron")
        ignore_columns.append("events")
        trial_data = trial_data.drop(columns=ignore_columns, level=0)
        single_trial = self._aggregate_trials(trial_data)
        assert single_trial is not None
        _, trial_data = single_trial
        self._dataset.trial_data = trial_data

    @staticmethod
    def _aggregate_trials(
        trial_data: pd.DataFrame,
    ) -> Optional[Tuple[str, pd.DataFrame]]:
        """combine corresponding trials across different pprox files

        if all trials contain the same data, return one trial
        otherwise, raise a IncompatibleTrialError
        """
        trials = trial_data.groupby(axis=1, level=1)
        first = None
        for name, t in trials:
            t = t.droplevel(axis=1, level=1)
            if first is None:
                first = (name, t)
            first_name, first_df = first
            if not first_df.equals(t):
                raise IncompatibleTrialError({first_name: first_df, name: t})
        return first

    def _extrapolate_bins(self, stim_name, interval):
        """ Extrapolate the bins defined over a stimulus interval to the recorded interval """
        # The assumption is that the bins are evenly spaced.

    def bin_responses(self, normalize: bool = True):
        """
        transform a point process into bins containing the number of events (or if `normalize` 
        is True, the rate of events) that occurred within the time bin. Time bins are set based on
        the stimulus, so this has to be called after add_stimuli()
        """
        trials = self._dataset._get_trial_data()
        spike_times = self._dataset._get_responses()
        stimuli = self._dataset._get_stimuli()

        def cut(df):
            stim_name = df["stimulus.name"]
            interval = df["interval"]
            stim_bins = stimuli.loc[stim_name].index.to_numpy()
            time_step = stim_bins[1] - stim_bins[0]
            edges = np.concatenate([
                np.arange(stim_bins[0], interval[0] - time_step, -time_step)[:0:-1],
                stim_bins,
                np.arange(stim_bins[-1], interval[-1] + time_step, time_step)[1:]
            ])
            arr = np.block(
                df[spike_times.columns]
                .apply(
                    lambda spikes: np.histogram(spikes, bins=edges)[0].reshape(-1, 1)
                )
                .to_numpy()
                .tolist()
            )
            if normalize:
                arr = arr / time_step
            return pd.DataFrame(
                arr,
                index=pd.MultiIndex.from_product(
                    [[df.name], edges[:-1]], names=["trial", "time"]
                ),
                columns=spike_times.columns,
            )
        self._dataset.responses = pd.concat(
            [cut(df) for _, df in spike_times.join(trials).iterrows()]
        )

    def add_stimuli(
        self, stimuli_format: StimuliFormat, time_step: float
    ):
        """
        Add a dataframe containing formatted stimuli for each
        stimulus associated with a trial

        Consult documentation for `preconstruct.stimuliformats` for details.

        ###### example
        <!--
        >>> import asyncio
        >>> from preconstruct.sources import NeurobankSource
        >>> responses = ['P120_1_1_c92']
        >>> url = 'https://gracula.psyc.virginia.edu/neurobank/'
        >>> stimuli = ['c95zqjxq', 'g29wxi4q', 'igmi8fxa', 'jkexyrd5', 'l1a3ltpy',
        ...         'mrel2o09', 'p1mrfhop', 'vekibwgj', 'w08e1crn', 'ztqee46x']
        >>> data_source = asyncio.run(NeurobankSource.create(url, stimuli, responses))
        >>> builder = DatasetBuilder()
        >>> builder.set_data_source(data_source)
        >>> builder.load_responses()

        -->
        >>> from preconstruct.stimuliformats import Gammatone
        >>> builder.add_stimuli(Gammatone(
        ...     window_time=0.001,
        ...     frequency_bin_count=50,
        ...     min_frequency=500,
        ...     max_frequency=8000,
        ... ), time_step=0.005) # 5 ms

        """
        self._dataset.stimuli_format = stimuli_format
        self._dataset.stimuli = stimuli_format.create_dataframe(
            self.data_source,
            time_step,
            self._dataset._get_trial_data()[["stimulus.name", "stimulus.interval"]]
            .drop_duplicates()
            .set_index("stimulus.name")["stimulus.interval"],
        )
        time_steps = (
            self._dataset.stimuli.index.to_frame()
            .groupby(0)
            .apply(lambda df: df[1].diff().mean())
        )
        if ((time_steps - time_steps[0]).abs() > 1e-9).any():
            raise IncompatibleStimulusSamplingRates

    def create_time_lags(self, tau: float = 0.300, basis: Optional[Basis] = None):
        """
        `tau`: length of window (in secs) to consider in prediction
        `basis`: an instance of a class that inherits from
        `preconstruct.basisfunctions.Basis`, initialized with the dimension
        of the projection

        ###### example
        <!--
        >>> import asyncio
        >>> from preconstruct.sources import NeurobankSource
        >>> from preconstruct.stimuliformats import Gammatone
        >>> responses = ['P120_1_1_c92']
        >>> url = 'https://gracula.psyc.virginia.edu/neurobank/'
        >>> stimuli = ['c95zqjxq', 'g29wxi4q', 'igmi8fxa', 'jkexyrd5', 'l1a3ltpy',
        ...         'mrel2o09', 'p1mrfhop', 'vekibwgj', 'w08e1crn', 'ztqee46x']
        >>> data_source = asyncio.run(NeurobankSource.create(url, stimuli, responses))
        >>> builder = DatasetBuilder()
        >>> builder.set_data_source(data_source)
        >>> builder.load_responses()
        >>> builder.bin_responses(time_step=0.005) # 5 ms
        >>> builder.add_stimuli(Gammatone())


        -->
        >>> from preconstruct.basisfunctions import RaisedCosineBasis
        >>> builder.create_time_lags(tau=0.3, basis=RaisedCosineBasis(30))


        """
        self.tau = tau
        self.basis = None
        if basis is not None:
            window_length = self._dataset.to_steps(self.tau)
            self.basis = basis.get_basis(window_length)
        # figure out if trials have been pooled and adjust accordingly
        common_index = self._dataset._get_responses().index.names[0]
        self._dataset.responses = (
            self._dataset._get_responses()
            .groupby(level=0, axis=1)
            .apply(
                lambda neuron: self._dataset._get_trial_data()[
                    ["stimulus.interval", "stimulus.name"]
                ]
                .merge(
                    neuron[neuron.columns[0]]  # convert to series
                    .rename("events")
                    .reset_index(level="time"),
                    on=common_index,
                    how="left",
                )
                .join(
                    self._dataset._get_stimuli()
                    .groupby(level=0)
                    .apply(lambda x: x.shape[0])
                    .rename("stimulus.length"),
                    on="stimulus.name",
                )
                .groupby(common_index)
                .apply(self._stagger)
            )
        )

    def _stagger(self, df):
        df = df.reset_index()
        [stimulus_interval] = df["stimulus.interval"].unique()
        stim_start, _ = stimulus_interval
        start = df["time"][df["time"] >= stim_start].idxmin()
        window_length = self._dataset.to_steps(self.tau)
        [stimulus_length] = df["stimulus.length"].unique()
        stop = start + stimulus_length
        events = df["events"]
        assert len(events) >= stop - 1 + window_length
        time_lagged = hankel(
            events[start:stop], events[stop - 1 : stop - 1 + window_length]
        )
        columns = pd.Series(
            np.arange(window_length) * self._dataset._get_time_step(), name="offset"
        )
        if self.basis is not None:
            time_lagged = np.dot(time_lagged, self.basis)
            columns = None
        return pd.DataFrame(
            time_lagged,
            index=df["time"].iloc[start:stop],
            columns=columns,
        )

    def pool_trials(self):
        """Pool spikes across trials"""
        if (
            not self._dataset._get_trial_data()
            .groupby("stimulus.name")["stimulus.interval"]
            .apply(lambda ser: len(ser.unique()) == 1)
            .all()
        ):
            raise InconsistentStimulusInterval

        responses = self._dataset._get_responses().reset_index()
        if "time" not in responses.columns:
            raise InvalidConstructionSequence("bin_responses")
        responses["stimulus.name"] = responses["trial"].map(
            self._dataset._get_trial_data()["stimulus.name"]
        )
        del responses["trial"]
        responses = responses.set_index(["stimulus.name", "time"]).sort_index()
        self._dataset.responses = responses.groupby(["stimulus.name", "time"]).agg(
            "sum"
        )

    def get_dataset(self) -> Dataset:
        """Return the fully constructed `Dataset` object"""
        return self._dataset


class _EmptySource(DataSource):
    def _get_raw_responses(self):
        self._raise()

    def get_stimuli(self):
        self._raise()

    @staticmethod
    def _raise():
        raise InvalidConstructionSequence("DatasetBuilder.set_data_source")


class InvalidConstructionSequence(Exception):
    """Indicates that the methods of a DatasetBuilder have been called in an invalid order"""

    def __init__(self, required_method):
        super().__init__()
        self.required_method = required_method

    def __str__(self) -> str:
        return (
            f"invalid construction sequence: must call `{self.required_method}` first"
        )


class IncompatibleTrialError(Exception):
    """Raised when corresponding trials from different pprox files differ

    If the differing trial data is expected, you can choose to not include
    specific keys using the `ignore_columns` argument in
    `DatasetBuilder.load_responses`.
    """

    def __init__(self, trial_pair: Dict[str, pd.DataFrame]):
        super().__init__()
        self.trial_pair = trial_pair

    def __str__(self) -> str:
        a, b = tuple(self.trial_pair.keys())
        return (
            f"at least two trials contained conflicting data: {a}, {b}\n"
            f"{self.trial_pair[a].compare(self.trial_pair[b])}"
        )


class InconsistentStimulusInterval(Exception):
    """Raised when stimulus.interval differs between trials that are to be combined"""

    def __str__(self) -> str:
        return (
            "if you want to pool trials, every stimulus presentation must have"
            " the same stimulus.interval"
        )


class IncompatibleStimulusSamplingRates(Exception):
    """Raised when it's not possible for all stimuli to have the desired time step"""

    def __str__(self) -> str:
        return (
            "Stimuli have different sampling rates, and it's not possible for"
            " them to all have the same time step"
        )


class IncompatibleStimuliFormat(Exception):
    def __init__(self, format):
        self.format = format

    def __str__(self) -> str:
        return (
            f"the StimuliFormat you have picked ({self.format})"
            " is not a subclass of `SameTimeIndexAsResponse`"
            " so you can't call this function"
        )


class TimestepSetTwice(Exception):
    def __init__(self):
        super().__init__(self, "You can only set time_step once")
