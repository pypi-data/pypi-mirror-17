# -*- coding: utf-8 -*-
"""
.. module:: colorview2d.cvfig
    :synopsis: The cvfig module hosts the CvFig class, the central object of cv2d.

"""
import logging
import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import yaml

from colorview2d import Datafile
import colorview2d.utils as utils

# setup logging

LOGGER = logging.getLogger('colorview2d')
LOGGER.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
FHAND = logging.FileHandler('spam.log')
FHAND.setLevel(logging.DEBUG)
# create console handler with a higher log level
CHAND = logging.StreamHandler()
CHAND.setLevel(logging.ERROR)
# create formatter and add it to the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FHAND.setFormatter(FORMATTER)
CHAND.setFormatter(FORMATTER)
# add the handlers to the logger
LOGGER.addHandler(FHAND)
LOGGER.addHandler(CHAND)


class CvFig(object):
    """
    .. class:: CvFig(data[, axes_bounds])

    A class to handle a 2d :class:`numpy.ndarray` with (linearly scaled) axes, apply a (extendable)
    range of filters (mods) to the data while keeping track of the
    modifications.

    Hosts a :class:`matplotlib.pyplot.Figure`. Customization of this figure
    is simplified with respect to the matplotlib library.

    Attributes:
        modlist (list): a list of all mods that can be found in the mods/ subfolder.
        datafile (:class:`colorview2d.Datafile`): the colorview2d datafile object encapsulates the 2d data.
        pipeline (dict): a dictionary with mod identifiers (strings) and their arguments (tuples).
        _config (dict): the configuration of the _plot details, colormap, fonts, etc.
        fig (:class:`matplotlib.pyplot.Figure`): The matplotlib figure of the data with axes.

    Example::
        datafile = colroview2d.Datafile(np.random.random((100, 100)))
        fig = colorview2d.cvfig.CvFig(datafile)
        fig.plot_pdf('Test.pdf')


    """
    def __init__(self, data=None,
                 cfgfile=None,
                 config=None,
                 pipeline=None):

        self._modlist = {}
        self._create_modlist()

        self._datafile = None
        
        if isinstance(data, np.ndarray):
            self._datafile = Datafile(data)
        elif isinstance(data, Datafile):
            self.datafile = data
        else:
            raise ValueError("Provide data or datafile to create a CvFig object.")
        self._original_datafile = self._datafile.deep_copy()

        # Holds information on the plot layout, ticks, fonts etc.
        self._config = utils.Config()
        # overwrite the on_change hook of the Config class.
        # this way we can react to changes in the config appropriately.
        self._config.on_change = self._on_config_change
            
        # The pipeline contains a dict of numbers and tuples with
        # strings that are unique to IMod objects
        # and their arguments
        self._pipeline = []

        if cfgfile:
            # If a config file is provided, we load that one.
            # All other parameters are ignored.
            # Note: The filename must be removed from the config file
            self.load_config(os.path.join(os.getcwd(), cfgfile))


        # if the config argument is not empty we replace the values
        if config:
            self._config.update_raw(config)

        # Matplotlib figure object, contains the actual plot
        # Generated upon retrieval by property accessor
        # Readonly, Initialized with one pixel
        plt.ioff()
        self._fig = plt.figure(1, dpi=self._config['Dpi'])

        # We use the property setter to add the given pipeline.
        if pipeline is not None:
            self.pipeline = pipeline

        self.apply_pipeline()


    @property
    def modlist(self):
        return self._modlist
        
    @property
    def datafile(self):
        return self._datafile

    @datafile.setter
    def datafile(self, datafile):
        """Sets the datafile.
        The original datafile is replaced as well and the modlist is applied.

        Args:
            datafile (colorview2d.Datafile): a Datafile object
        """
        self._datafile = datafile
        self._datafile_changed()


    def _datafile_changed(self):
        """Called when the datafile is modified."""

        if self.plotting:
            self._plot.set_data(self._datafile.zdata)
            self._plot.set_extent([self._datafile.xleft, self._datafile.xright,
                                   self._datafile.ybottom, self._datafile.ytop])
            self.axes.set_xlim(self._datafile.xleft, self._datafile.xright)
            self.axes.set_ylim(self._datafile.ybottom, self._datafile.ytop)

            if self._config['Cbmin'] == 'auto':
                # re-setting the value triggers update of the plot
                self._config['Cbmin'] = 'auto'
            if self._config['Cbmax'] == 'auto':
                # re-setting the value triggers update of the plot
                self._config['Cbmax'] = 'auto'
            self._plot.changed()
        return

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config_dict):
        """Change the config. Note that it is a custom :class:`colorview2d.utils.ConfigDict` class.
        We use the update routine to prevent overwriting the private attribute with
        an ordinary :class:`dict`

        Anyways: Be careful when overwriting the config because there is no error checking
        on the values given!

        Args:
            config_dict (dict): dictionary with configuration items.
        """
        self._config.update(config_dict)

    @property
    def fig(self):
        """Retrieve the matplotlib figure."""
        if not hasattr(self, '_plot'):
            self.draw_plot()
        return self._fig

    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        """Overwrite the pipeline string. Note that this is used for initialization
        and does not trigger any modifications to the datafile.

        Args:
            pipeline (list): A list of strings that are valid mod identifiers.
        """
        self._pipeline = []

        for modstring in pipeline:
            self.add_mod(modstring[0], modstring[1])

    @property
    def plotting(self):
        """Determine if we are showing any plot at the moment."""
        # We use the existence of the private _plot attribute
        # as a primer.
        return hasattr(self, '_plot')

    # def show(self):
    #     """Show the figure in the GUI.
    #     Can be used only if wxpython is installed.

    #     The GUI is not yet functional.
    #     """

    #     try:
    #         import colorview2d.mainapp as mainapp
    #     except ImportError:
    #         logging.error('Cannot start the GUI. Is wxpython installed?')
    #         return

    #     logging.info("Initializing the GUI.")
    #     self.mainapp = mainapp.MainApp(self)
    #     self.mainapp.MainLoop()

    def show_plt_fig(self):
        """Show the interactive :class:`matplotlib.pyplot.Figure`.

        Note: Due to a bug in matplotlib it is not possible to re-show
        a figure once it was hidden with Tk as backend.
        """
        self.draw_plot()
        plt.ion()

        # in order to successively open and close the
        # interactive figure, we have to
        # create a dummy figure and use its
        # manager to display "fig"

        if not self.plt_fig_is_active():
            dummy_fig = plt.figure()
            self._fig_manager = dummy_fig.canvas.manager
            self._fig_manager.canvas.figure = self._fig
            self._fig.set_canvas(self._fig_manager.canvas)
            self._fig.show()


    def plt_fig_is_active(self):
        """Check if there is an active canvas manager.
        If there is, we are (hopefully) running an active matplotlib.pyplot window
        with an interactive plot.
        """
        return hasattr(self, '_fig_manager')


    def hide_plt_fig(self):
        """Hide the interactive :class`matplotlib.pyplot.Figure`.
        The method deletes the canvas.manager of the current figure
        and the plot object if present.

        Note: Due to a bug in matplotlib it is not possible to re-show
        a figure once it was hidden with Tk as backend.
        """
        # To this end we have to destroy the figure manager.
        # See maptlotlib.pyplot.close().
        if self.plt_fig_is_active():
            plt._pylab_helpers.Gcf.destroy(self._fig_manager.num)
            delattr(self, '_fig_manager')
        # we delete _plot which indicates that we are not plotting
        if hasattr(self, '_plot'):
            delattr(self, '_plot')

    def _create_modlist(self):
        """
        Creates the list of mods from the mods/ folder and adds them
        to the private modlist attribute.

        We check if the module (with arbitrary name) contains a class
        which inherits from colorview2d.IMod
        """
        import pkgutil
        import inspect

        import colorview2d.mods

        package = colorview2d.mods
        for importer, modname, ispckg in pkgutil.iter_modules(package.__path__):
            try:    
                mod = importer.find_module(modname).load_module(modname)
                for name, obj in inspect.getmembers(mod):
                    if inspect.isclass(obj):
                        if issubclass(obj, colorview2d.IMod):
                            self._modlist[name] = obj()
            except:
                error = sys.exc_info()[0]
                logging.error('Can not import mod %s.', modname)
                logging.error('Error: %s.', error)
        # import ipdb;ipdb.set_trace()


    def add_mod(self, modname, modargs=(),  pos=-1, do_apply=True):
        """Adds a mod to the pipeline by its title string and its arguments.

        Args:
            modname (string): The type of the mod.
            modargs (tuple): A tuple containing the arguments of the mod.
            pos (int): Where to add the mod in the pipeline. Default is last.
            do_apply (boolean): Trigger modification of the datafile (True) or just add
                mod to the pipeline.
        """

        logging.info('Add mod %s to pipeline with arguments %s' % (modname, modargs))
        modstring = (modname, modargs)

        if self._modlist[modname]:
            if pos == -1:
                self._pipeline.append(modstring)
            elif pos < len(self._pipeline) and pos >= 1:
                self._pipeline.insert(pos - 1, modstring)
            else:
                logging.warn('Position %d not available in pipeline.' % pos)
        else:
            logging.warn('Mod %s not available in mod plugin list.' % title)

        if do_apply:
            self.apply_pipeline()

    def remove_mod(self, modtype=None, pos=-1,  do_apply=True):
        """Removes the last mod from the pipeline, or the mod at position pos
        or the last mod in the pipeline with the type modtype.

        Args:
            modtype (string): The identifier of the mod type.
            pos (int): The position of the mod in the pipeline.
            do_apply (bool): Is the pipeline applied after the element is removed?
        """

        if pos == -1 and not modtype:
            self._pipeline.pop()
        elif pos >= 1 and pos <= len(self._pipeline):
            del self._pipeline[pos - 1]
        elif modtype:
            found = False
            for modtuple in reversed(self._pipeline):
                if modtuple[0] == modtype:
                    self._pipeline.remove(modtuple)
                    found = True
            if not found:
                logging.warn('Mod %s not in current pipeline.' % modtype)
        else:
                logging.warn('Pos = %d is not a valid position.' % pos)

        if do_apply:
            self.apply_pipeline()

    def apply_pipeline(self):
        """Applies the pipeline to the datafile in the parent frame.

        The datafile is first reverted to its original state,
        then mods are applied in the order they were added.
        The plot panel is notified of the update in the datafile.
        The main panel is signalled to update the color controls.
        """

        self._datafile = self._original_datafile.deep_copy()

        for pos, modtuple in enumerate(self._pipeline):
            mod = self._modlist[modtuple[0]]
            if mod:
                # if apply returns false, the application failed and the
                # mod is removed from the pipeline
                if not mod.apply(self._datafile, modtuple[1]):
                    logging.warning(
                        'Application of mod %s at position %d failed.'
                        'Removing mod from pipeline.' % (mod.title, pos))
                    self.remove_mod(pos)
                self._datafile_changed()
            else:
                logging.warning('No mod candidate found for %s.', modtuple[0])


    def get_arraydata(self):
        """Shortcut for the 2d data contained int the datafile.
        Interface for plotting routine.
        """
        return self.datafile.zdata


    def load_config(self, cfgpath):
        """Load the configuration and the pipeline from the config file
        specified in the YAML format. 

        Args:
            cfgpath (string): The path to a cv2d configuration file.
        """
        from ast import literal_eval

        with open(cfgpath) as cfgfile:
            doclist = yaml.load_all(cfgfile)
            # The config dict is the first yaml document

            self._config.update_raw(doclist.next())
            if self.plotting:
                self.draw_plot()
            # The pipeline string is the second. It is optional.
            try:
                logging.info('Pipeline string found: %s', self.pipeline)
                pipeline = literal_eval(doclist.next())
                # Note that the property setter is called
                # applying the mods one by one
                self.pipeline = pipeline

            except StopIteration:
                logging.info('No pipeline string found.')


    def save_config(self, cfgpath):
        """Save the configuration and the pipeline to a config file specified by
        cfgpath.

        Args:
            cfgpath (string): the path to the config file
        """
        with open(cfgpath, 'w') as stream:
            # We write first the config dict
            yaml.dump(self._config.dict, stream, explicit_start=True)
            # ... and second the pipeline string
            yaml.dump(repr(self._pipeline), stream, explicit_start=True)

    def _on_config_change(self, key, value):
        # When there is no plot we do not care at the moment.
        if not self.plotting:
            return
            
        if key == 'Colormap':
            self._plot.set_cmap(self._config['Colormap'])
        elif key == 'Cbmin':
            if value == 'auto':
                self._plot.set_clim(vmin=self._datafile.zmin)
            else:
                self._plot.set_clim(vmin=self._config['Cbmin'])
        elif key == 'Cbmax':
            if value == 'auto':
                self._plot.set_clim(vmax=self._datafile.zmax)
            else:
                self._plot.set_clim(vmax=self._config['Cbmax'])

        if key in ['Colormap', 'Cbmin', 'Cbmax']:
            self._plot.changed()
            return

        # If config_dict only contains changes that do not need a redrawing
        # of the plot we apply them and return
        if key in ['Xlabel', 'Ylabel', 'Xtickformat', 'Ytickformat', 'Cblabel']:
            self._apply_config_post_plot()
            return

        # If the font parameters, the ticksize or the format of the colorbar ticks
        # is changed, we have to redraw the plot
        self.draw_plot()

    def plot_pdf(self, filename):
        """Redraw the figure and plot it to a pdf file."""
        self.draw_plot()
        self._fig.set_size_inches(self._config['Width'], self._config['Height'])
        self._fig.tight_layout()
        self._fig.savefig(filename, dpi=self._config['Dpi'])

    def draw_plot(self):
        """Draw a matplotlib figure.

        The figure is stored in the fig attribute.
        In includes an axes object containing the (imshow generated)
        2d color plot with labels, ticks and colorbar as specified in the
        config dictionary..
        """
        self._fig.clear()
        self.axes = self._fig.add_subplot(111)
        self._apply_config_pre_plot()

        self._plot = self.axes.imshow(self.get_arraydata(),
            extent=[self.datafile.xleft,
                    self.datafile.xright,
                    self.datafile.ybottom,
                    self.datafile.ytop],
            aspect='auto',
            origin='lower',
            interpolation="nearest")

        if not self._config['Cbtickformat'] == 'auto':
            self.colorbar = self._fig.colorbar(
                self._plot,
                format=FormatStrFormatter(self._config['Cbtickformat']))
        else:
            self.colorbar = self._fig.colorbar(self._plot)

        # we set the correct colorbar settings
        # this call seems redundant but invokes the update
        # of the colorbar
        self.config = {'Cbmin':self.config['Cbmin'], 'Cbmax':self.config['Cbmax']}

        self._apply_config_post_plot()

        self._plot.changed()
        self._fig.tight_layout()


    def _apply_config_post_plot(self):
        """
        The function applies the rest of the configuration to the plot.
        Note that the colorbar is created in this function because
        colorbar.ax.yaxis.set_major_formatter(FormatStrFormatter(string)) does not work properly.
        """
        self.axes.set_ylabel(self._config['Ylabel'])
        self.axes.set_xlabel(self._config['Xlabel'])

        self.colorbar.set_label(self._config['Cblabel'])
        if not self._config['Xtickformat'] == 'auto':
            self.axes.xaxis.set_major_formatter(FormatStrFormatter(self._config['Xtickformat']))
        if not self._config['Ytickformat'] == 'auto':
            self.axes.yaxis.set_major_formatter(FormatStrFormatter(self._config['Ytickformat']))
        self._plot.set_cmap(self._config['Colormap'])



    def _apply_config_pre_plot(self):
        """
        Applies the ticks and labels stored in the MainFrame.
        This function is called before the actual plot is drawn.
        This pre_plot hook is necessary because the rcParams['font.family']
        attribute can not be changed after the plot is drawn.
        """

        logging.info("Font now {}".format(self._config['Font']))

        if self._config['Font'] is 'default':
            plt.rcParams.update(plt.rcParamsDefault)
        else:
            plt.rcParams['font.family'] = self._config['Font']
        plt.rcParams['font.size'] = self._config['Fontsize']
        plt.rcParams['xtick.major.size'] = self._config['Xticklength']
        plt.rcParams['ytick.major.size'] = self._config['Yticklength']

    
