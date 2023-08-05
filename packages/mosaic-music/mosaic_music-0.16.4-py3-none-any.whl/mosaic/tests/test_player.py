from mosaic import player, configuration, information
import pkg_resources
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog


@pytest.fixture
def window(qtbot):
    """Initializes the music player window for each test. Showing the window
    has the indirect effect of testing items assigned to the main window such
    as the menu bar and the toolbar. Since the window would crash if these items
    did not exist or did not show, they are covered by this setup method."""
    music_player = player.MusicPlayer()
    qtbot.add_widget(music_player)
    music_player.show()
    return music_player


@pytest.fixture
def file_config(qtbot):
    """Returns an instance of the File Options configuration page that can be
    passed as an argument to the unit tests."""
    config = configuration.FileOptions()
    qtbot.add_widget(config)
    return config


@pytest.fixture
def flac_file():
    """Returns a resource of the test FLAC file that can be passed as an argument
    to the unit tests."""
    file = pkg_resources.resource_filename('mosaic.tests', '02_Ghosts_I.flac')
    return file


@pytest.fixture
def mp3_file():
    """Returns a resource of the test MP3 file that can be passed as an argument
    to the unit tests."""
    file = pkg_resources.resource_filename('mosaic.tests', '01_Ghosts_I_320kb.mp3')
    return file


@pytest.fixture
def blank_flac_file():
    """Returns a resource of a test FLAC file that can be passed as an argument to the
    unit tests. The metadata from this file has been removed to test cases where a file
    has no metadata."""
    file = pkg_resources.resource_filename('mosaic.tests', '03_Ghosts_I.flac')
    return file


def test_window(window):
    """Asserts that the window contains the proper title as well as the
    propeer height and width. Also asserts that the window icon appears
    correctly."""
    assert window.windowTitle() == 'Mosaic'
    assert window.width() == 900
    assert window.height() == 963
    assert window.windowIcon().isNull() is False


def test_open_flac_file(qtbot, mock, window, flac_file):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open file item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=(flac_file, '*.flac'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_files(qtbot, mock, window, flac_file, mp3_file):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open files item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileNames', return_value=(
                      [flac_file, mp3_file], '*.flac *.mp3'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_playlist(qtbot, mock, window):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open playlist item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=('test.m3u', '*.m3u'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_directory(qtbot, mock, window):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open directory item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    file = pkg_resources.resource_filename('mosaic.tests', '')
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getExistingDirectory', return_value=file)
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_mp3_file(qtbot, mock, window, mp3_file):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open file item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=(mp3_file, '*.mp3'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_blank_file(qtbot, mock, window, blank_flac_file):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights the open file item.
    The mock plugin creates a mock of the QFileDialog window while Qt.Key_Enter executes it.
    This test opens a blank flac file to test cases where metadata is not embedded in the file."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=(blank_flac_file, '*.flac'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_quit_application(qtbot, monkeypatch, window):
    """Qtbot clicks on the file menu and Qt.Key_Down highlights the quit application
    item. Monkeypatch is set to intercept the exit call and will append 1 to exit_calls
    when it does."""
    exit_calls = []
    monkeypatch.setattr(QApplication, 'quit', lambda: exit_calls.append(1))
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Enter)
    assert exit_calls == [1]


def test_preferences(qtbot, mock, window):
    """Qtbot clicks on the edit menu then Qt.Key_Down highlights
    the preferences item. The mock plugin creates a mock of the
    QDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    mock.patch.object(QDialog, 'exec_', return_value='accept')
    qtbot.keyClick(window.edit, Qt.Key_Enter)


def test_about_dialog(qtbot, mock, window):
    """Qtbot clicks on the help menu then Qt.Key_Down highlights
    the about item. The mock plugin creates a mock of the
    QMessageBox window while Key_Enter executes it."""
    qtbot.mouseClick(window.help_, Qt.LeftButton)
    qtbot.keyClick(window.help_, Qt.Key_Down)
    mock.patch.object(QDialog, 'exec_', return_value='finished')
    qtbot.keyClick(window.help_, Qt.Key_Enter)


def test_playlist_view(qtbot, mock, window):
    """Qtbot selects the view menu then keys down to the view playlist
    item. Once highlighted, qtbot simulates the enter key on the item."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_media_information(qtbot, mock, window):
    """Qtbot clicks on the view menu then Qt.Key_Down highlights
    the media information item. The mock plugin creates a mock of the
    QDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    mock.patch.object(QDialog, 'exec_', return_value='finished')
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_media_library(qtbot, window):
    """Qtbot clicks on the view menu then navigates to the View Media Library
    item and uses Qt.Key_Enter to select it."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_media_information_directly(qtbot, flac_file, mp3_file):
    """Creates an instance of the GenralInformation and FullInformation classes to see
    if there are any errors."""
    information.GeneralInformation(flac_file)
    information.FullInformation(flac_file)
    information.GeneralInformation(mp3_file)
    information.FullInformation(mp3_file)
