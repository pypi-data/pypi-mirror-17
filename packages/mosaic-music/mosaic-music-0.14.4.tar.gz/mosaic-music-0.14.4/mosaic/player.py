from mosaic import about, configuration, defaults, information, library, metadata
import natsort
import os
import pkg_resources
from PyQt5.QtCore import Qt, QFileInfo, QTime, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDockWidget, QFileDialog,
                             QLabel, QListWidget, QListWidgetItem, QMainWindow, QSizePolicy,
                             QSlider, QToolBar, QVBoxLayout, QWidget)
import sys


class MusicPlayer(QMainWindow):
    """MusicPlayer houses all of the methods and attributes needed to
    instantiate a fully functional music player."""

    def __init__(self, parent=None):
        """Initializes the QMainWindow widget and calls methods that house
        other widgets that need to be displayed in the main window."""

        super(MusicPlayer, self).__init__(parent)
        self.setWindowTitle('Mosaic')
        window_icon = pkg_resources.resource_filename('mosaic.images', 'icon.png')
        self.setWindowIcon(QIcon(window_icon))
        self.resize(defaults.Settings().window_size(), defaults.Settings().window_size() + 63)

        # Initiates Qt objects to be used by MusicPlayer
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.content = QMediaContent()
        self.menu = self.menuBar()
        self.art = QLabel()
        self.pixmap = QPixmap()
        self.slider = QSlider(Qt.Horizontal)
        self.duration_label = QLabel()
        self.playlist_dock = QDockWidget('Playlist', self)
        self.library_dock = QDockWidget('Media Library', self)
        self.playlist_view = QListWidget()
        self.library_view = library.MediaLibraryView()
        self.library_model = library.MediaLibraryModel()
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.about = about.AboutDialog()
        self.duration = 0

        # Sets QWidget() as the central widget of the main window
        self.setCentralWidget(self.widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.art.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Initiates the playlist dock widget and the library dock widget
        self.addDockWidget(Qt.RightDockWidgetArea, self.playlist_dock)
        self.playlist_dock.setWidget(self.playlist_view)
        self.playlist_dock.resize(300, 800)
        self.playlist_dock.setVisible(False)
        self.playlist_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.addDockWidget(Qt.RightDockWidgetArea, self.library_dock)
        self.library_dock.setWidget(self.library_view)
        self.library_dock.resize(400, 800)
        self.library_dock.setVisible(defaults.Settings().media_library_on_start())
        self.library_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.tabifyDockWidget(self.playlist_dock, self.library_dock)

        # Sets the range of the playback slider and sets the playback mode as looping
        self.slider.setRange(0, self.player.duration() / 1000)
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)

        # Initiates Settings in the defaults module to give access to settings.toml
        defaults.Settings()

        # Signals that connect to other methods when they're called
        self.player.metaDataChanged.connect(self.display_meta_data)
        self.slider.sliderMoved.connect(self.seek)
        self.player.durationChanged.connect(self.song_duration)
        self.player.positionChanged.connect(self.song_position)
        self.player.stateChanged.connect(self.set_state)
        self.playlist_view.itemActivated.connect(self.playlist_item)
        self.library_view.activated.connect(self.open_media_library)
        self.playlist.currentIndexChanged.connect(self.change_index)
        self.playlist_dock.visibilityChanged.connect(self.dock_visiblity_change)
        self.library_dock.visibilityChanged.connect(self.dock_visiblity_change)
        self.art.mousePressEvent = self.press_playback

        # Creating the menu controls, media controls, and window size of the music player
        self.menu_controls()
        self.media_controls()

    def menu_controls(self):
        """Initiates the menu bar and adds it to the QMainWindow widget."""

        self.file = self.menu.addMenu('File')
        self.edit = self.menu.addMenu('Edit')
        self.view = self.menu.addMenu('View')
        self.help_ = self.menu.addMenu('Help')

        self.file_menu()
        self.edit_menu()
        self.view_menu()
        self.help_menu()

    def media_controls(self):
        """Creates the bottom toolbar and controls used for media playback."""

        self.toolbar = QToolBar()
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)

        play_icon = pkg_resources.resource_filename('mosaic.images', 'md_play.png')
        self.play_action = QAction(QIcon(play_icon), 'Play', self)
        self.play_action.triggered.connect(self.player.play)

        stop_icon = pkg_resources.resource_filename('mosaic.images', 'md_stop.png')
        self.stop_action = QAction(QIcon(stop_icon), 'Stop', self)
        self.stop_action.triggered.connect(self.player.stop)

        previous_icon = pkg_resources.resource_filename('mosaic.images', 'md_previous.png')
        self.previous_action = QAction(QIcon(previous_icon), 'Previous', self)
        self.previous_action.triggered.connect(self.playlist.previous)

        next_icon = pkg_resources.resource_filename('mosaic.images', 'md_next.png')
        self.next_action = QAction(QIcon(next_icon), 'Next', self)
        self.next_action.triggered.connect(self.playlist.next)

        repeat_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat.png')
        self.repeat_action = QAction(QIcon(repeat_icon), 'Repeat', self)
        self.repeat_action.triggered.connect(self.repeat_song)

        self.toolbar.addAction(self.play_action)
        self.toolbar.addAction(self.stop_action)
        self.toolbar.addAction(self.previous_action)
        self.toolbar.addAction(self.next_action)
        self.toolbar.addAction(self.repeat_action)
        self.toolbar.addWidget(self.slider)
        self.toolbar.addWidget(self.duration_label)

    def file_menu(self):
        """Adds a file menu to the menu bar. Allows the user to choose actions
        related to audio files."""

        self.open_action = QAction('Open File', self)
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.open_multiple_files_action = QAction('Open Multiple Files', self)
        self.open_multiple_files_action.setShortcut('CTRL+SHIFT+O')
        self.open_multiple_files_action.triggered.connect(self.open_multiple_files)

        self.open_playlist_action = QAction('Open Playlist', self)
        self.open_playlist_action.setShortcut('CTRL+P')
        self.open_playlist_action.triggered.connect(self.open_playlist)

        self.open_directory_action = QAction('Open Directory', self)
        self.open_directory_action.setShortcut('CTRL+D')
        self.open_directory_action.triggered.connect(self.open_directory)

        self.exit_action = QAction('Quit', self)
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(lambda: QApplication.quit())

        self.file.addAction(self.open_action)
        self.file.addAction(self.open_multiple_files_action)
        self.file.addAction(self.open_playlist_action)
        self.file.addAction(self.open_directory_action)
        self.file.addSeparator()
        self.file.addAction(self.exit_action)

    def edit_menu(self):
        """Provides items that allow the user to customize
        the options of the music player."""

        self.preferences_action = QAction('Preferences', self)
        self.preferences_action.setShortcut('CTRL+SHIFT+P')
        self.preferences_action.triggered.connect(lambda: configuration.PreferencesDialog().exec_())

        self.edit.addAction(self.preferences_action)

    def view_menu(self):
        """Provides items that allow the user to customize the viewing
        experience of the main window."""

        self.dock_action = self.playlist_dock.toggleViewAction()
        self.dock_action.setShortcut('CTRL+ALT+P')

        self.library_dock_action = self.library_dock.toggleViewAction()
        self.library_dock_action.setShortcut('CTRL+ALT+L')

        self.view_media_info_action = QAction('Media Information', self)
        self.view_media_info_action.setShortcut('CTRL+SHIFT+M')
        self.view_media_info_action.triggered.connect(self.media_information_dialog)

        self.view.addAction(self.dock_action)
        self.view.addAction(self.library_dock_action)
        self.view.addSeparator()
        self.view.addAction(self.view_media_info_action)

    def help_menu(self):
        """Provides informational items regarding the application."""

        self.about_action = QAction('About', self)
        self.about_action.setShortcut('CTRL+H')
        self.about_action.triggered.connect(lambda: self.about.exec_())

        self.help_.addAction(self.about_action)

    def open_file(self):
        """Opens the selected file and adds it to a new playlist."""

        filename, ok = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'Audio (*.mp3 *.flac)', '',
            QFileDialog.ReadOnly)
        if ok:
            file_info = QFileInfo(filename).fileName()
            playlist_item = QListWidgetItem(file_info)
            self.playlist.clear()
            self.playlist_view.clear()
            self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(filename)))
            self.player.setPlaylist(self.playlist)
            playlist_item.setToolTip(file_info)
            self.playlist_view.addItem(playlist_item)
            self.playlist_view.setCurrentRow(0)
            self.player.play()

    def open_multiple_files(self):
        """Opens the selected files and adds them to a new playlist."""

        filenames, ok = QFileDialog.getOpenFileNames(
            self, 'Open Multiple Files', '',
            'Audio (*.mp3 *.flac)', '', QFileDialog.ReadOnly)
        if ok:
            self.playlist.clear()
            self.playlist_view.clear()
            for file in natsort.natsorted(filenames, alg=natsort.ns.PATH):
                file_info = QFileInfo(file).fileName()
                playlist_item = QListWidgetItem(file_info)
                self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                self.player.setPlaylist(self.playlist)
                playlist_item.setToolTip(file_info)
                self.playlist_view.addItem(playlist_item)
                self.playlist_view.setCurrentRow(0)
                self.player.play()

    def open_playlist(self):
        """Loads an m3u or pls file into an empty playlist and adds the
        content of the chosen playlist to playlist_view."""

        playlist, ok = QFileDialog.getOpenFileName(
            self, 'Open Playlist', '',
            'Playlist (*.m3u *.pls)', '', QFileDialog.ReadOnly)
        if ok:
            playlist = QUrl.fromLocalFile(playlist)
            self.playlist.clear()
            self.playlist_view.clear()
            self.playlist.load(playlist)
            self.player.setPlaylist(self.playlist)

            for song_index in range(self.playlist.mediaCount()+1):
                file_info = self.playlist.media(song_index).canonicalUrl().fileName()
                playlist_item = QListWidgetItem(file_info)
                playlist_item.setToolTip(file_info)
                self.playlist_view.addItem(playlist_item)

            self.player.play()

    def open_directory(self):
        """Opens the chosen directory and adds supported audio filetypes within
        the directory to an empty playlist."""

        directory = QFileDialog.getExistingDirectory(
            self, 'Open Directory', '', QFileDialog.ReadOnly)
        if directory:
            self.playlist.clear()
            self.playlist_view.clear()
            for dirpath, __, files in os.walk(directory):
                for filename in natsort.natsorted(files, alg=natsort.ns.PATH):
                    file = os.path.join(dirpath, filename)
                    if filename.endswith(('mp3', 'flac')):
                        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                        playlist_item = QListWidgetItem(filename)
                        playlist_item.setToolTip(filename)
                        self.playlist_view.addItem(playlist_item)

            self.player.setPlaylist(self.playlist)
            self.playlist_view.setCurrentRow(0)
            self.player.play()

    def open_media_library(self, index):
        """Allows the user to add a directory or audio file from the media library
        to a new playlist."""

        self.playlist.clear()
        self.playlist_view.clear()

        if self.library_model.fileName(index).endswith(('mp3', 'flac')):
            self.playlist.addMedia(
                QMediaContent(QUrl().fromLocalFile(self.library_model.filePath(index))))
            self.playlist_view.addItem(self.library_model.fileName(index))

        elif self.library_model.isDir(index):
            directory = self.library_model.filePath(index)
            for dirpath, __, files in os.walk(directory):
                for filename in natsort.natsorted(files, alg=natsort.ns.PATH):
                    file = os.path.join(dirpath, filename)
                    if filename.endswith(('mp3', 'flac')):
                        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                        playlist_item = QListWidgetItem(filename)
                        playlist_item.setToolTip(filename)
                        self.playlist_view.addItem(playlist_item)

        self.player.setPlaylist(self.playlist)
        self.playlist_dock.setVisible(True)
        self.playlist_dock.show()
        self.playlist_dock.raise_()
        self.player.play()

    def display_meta_data(self):
        """QPixmap() is initiated in order to send an image to QLabel() which then
        displays the image in QMainWindow. When a file is loaded, this function
        affirms that meta data in the audio file exists."""

        if self.player.isMetaDataAvailable():
            file_path = self.player.currentMedia().canonicalUrl().toLocalFile()
            (album, artist, title, track_number, *__, artwork) = metadata.metadata(file_path)

            try:
                self.pixmap.loadFromData(artwork)
            except TypeError:
                self.pixmap = QPixmap(artwork)

            meta_data = '{} - {} - {} - {}' .format(
                    track_number, artist, album, title)
            self.setWindowTitle(meta_data)

            self.art.setScaledContents(True)
            self.art.setPixmap(self.pixmap)

            self.layout.addWidget(self.art)

    def press_playback(self, event):
        """On mouse event, the player will play the media if the player is
        either paused or stopped. If the media is playing, the media is set
        to pause."""

        if (self.player.state() == QMediaPlayer.StoppedState or
                self.player.state() == QMediaPlayer.PausedState):
            self.player.play()
        elif self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()

    def seek(self, seconds):
        """When the user drags the horizontal slider, this function sets
        the position of the song to the position dragged to."""

        self.player.setPosition(seconds * 1000)

    def song_duration(self, duration):
        """Sets the slider to the duration of the currently played media."""

        duration /= 1000
        self.duration = duration
        self.slider.setMaximum(duration)

    def song_position(self, progress):
        """As the song plays, the slider moves in sync with the duration
        of the song. The progress is relayed to update_duration() in order
        to display the time label next to the slider."""

        progress /= 1000

        if not self.slider.isSliderDown():
            self.slider.setValue(progress)

        self.update_duration(progress)

    def update_duration(self, current_duration):
        """Calculates the time played and length of the song in time. Both
        of these times are sent to duration_label() in order to display the
        times on the toolbar."""

        duration = self.duration

        if current_duration or duration:
            time_played = QTime((current_duration / 3600) % 60, (current_duration / 60) % 60,
                                (current_duration % 60), (current_duration * 1000) % 1000)
            song_length = QTime((duration / 3600) % 60, (duration / 60) % 60, (duration % 60),
                                (duration * 1000) % 1000)

            if duration > 3600:
                time_format = "hh:mm:ss"
            else:
                time_format = "mm:ss"

            time_display = "{} / {}" .format(time_played.toString(time_format),
                                             song_length.toString(time_format))
        else:
            time_display = ""

        self.duration_label.setText(time_display)

    def set_state(self, state):
        """Changes the play icon to the pause icon when a song is playing and
        changes the pause icon back to the play icon when either paused or
        stopped. The action of the button changes with respect to its icon."""

        if self.player.state() == QMediaPlayer.PlayingState:
            pause_icon = pkg_resources.resource_filename('mosaic.images', 'md_pause.png')
            self.play_action.setIcon(QIcon(pause_icon))
            self.play_action.triggered.connect(self.player.pause)
        elif (self.player.state() == QMediaPlayer.PausedState or
              self.player.state() == QMediaPlayer.StoppedState):
            self.play_action.triggered.connect(self.player.play)
            play_icon = pkg_resources.resource_filename('mosaic.images', 'md_play.png')
            self.play_action.setIcon(QIcon(play_icon))

    def repeat_song(self):
        """Sets the current media to repeat and changes the repeat icon
        accordingly."""

        if self.playlist.playbackMode() != QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            repeat_on_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat_on.png')
            self.repeat_action.setIcon(QIcon(repeat_on_icon))
        elif self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            repeat_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat.png')
            self.repeat_action.setIcon(QIcon(repeat_icon))

    def playlist_item(self, item):
        """Allows the user to play a song in the playlist by double clicking that item. If
        the media player is either paused or stopped, the song will start playing."""

        current_index = self.playlist_view.row(item)
        if self.playlist.currentIndex() != current_index:
            self.playlist.setCurrentIndex(current_index)

        if self.player.state() != QMediaPlayer.PlayingState:
            self.player.play()

    def change_index(self, row):
        """Changes the playlist view in relation to the current media."""

        self.playlist_view.setCurrentRow(row)

    def dock_visiblity_change(self, visible):
        """Changes the size of the main window when either the playlist dock or media library dock
        are opened. Reverts the main window back to its original size when both docks are closed."""

        if visible and self.playlist_dock.isVisible() and not self.library_dock.isVisible():
            self.resize(defaults.Settings().window_size() + self.playlist_dock.width() + 6,
                        self.height())

        elif visible and not self.playlist_dock.isVisible() and self.library_dock.isVisible():
            self.resize(defaults.Settings().window_size() + self.library_dock.width() + 6,
                        self.height())

        elif not visible and not self.playlist_dock.isVisible() and not self.library_dock.isVisible():
            self.resize(defaults.Settings().window_size(), defaults.Settings().window_size() + 63)

    def media_information_dialog(self):
        """If a song is currently playing, the file path of the song is sent to the
        media information dialog in order to show all of the avaialble metadata."""

        if self.player.isMetaDataAvailable():
            file_path = self.player.currentMedia().canonicalUrl().toLocalFile()
        else:
            file_path = None
        dialog = information.InformationDialog(file_path)
        dialog.exec_()


def main():
    """Creates an instance of the music player and uses QApplication to create the GUI.
    QDesktopWidget() is used to move the application to the center of the user's screen."""
    application = QApplication(sys.argv)
    window = MusicPlayer()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())
