from PyQt5 import QtCore, QtGui, QtWidgets

# ------------------------------------------------------------------------
#                           Global Constants
# ------------------------------------------------------------------------
MAIN_COLOR = "#455054"
SECONDARY_COLOR = "#FFF"

WINDOW_STYLE = f"background-color:{MAIN_COLOR}"
BUTTON_STYLE = """
    QPushButton {
        color: #fff;
        background-color: rgba(255, 255, 255, 0);
        border: 3px solid #fff;
        padding: 8px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 10);
    }
"""
LABEL_WHITE_TEXT = f"color:{SECONDARY_COLOR}"
GROUPBOX_WHITE_TEXT = f"color:{SECONDARY_COLOR}"

TITLE_FONT = QtGui.QFont("Didot", 30)
SIDEBAR_TITLE_FONT = QtGui.QFont("Didot", 25)
SECTION_FONT = QtGui.QFont("Didot", 18)
ITEM_NAME_FONT = QtGui.QFont("Didot", 14)

SLIDER_STYLESHEET = """
            QSlider::groove:horizontal {
                border: 1px solid #1D2731;
                height: 8px;
                background: #505F6F;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #FFFFFF;
                border: 2px solid #1D2731;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -4px 0; /* To center the handle properly */
            }

            QSlider::handle:horizontal:hover {
                background: #E0E0E0; /* Slightly lighter handle on hover */
            }

            QSlider::sub-page:horizontal {
                background: #6C7A8C; /* Filled portion of the slider (left of the handle) */
                border-radius: 4px;
            }

            QSlider::add-page:horizontal {
                background: #424242;/* Unfilled portion of the slider (right of the handle) */
                border-radius: 4px;
            }
"""
TABLE_STYLESHEET = f"""
    QTableWidget {{
        background-color: {MAIN_COLOR};
        color: {SECONDARY_COLOR};
        gridline-color: #D3D3D3;
        font-size: 14px;
        border: 1px solid #FFF;
        selection-background-color: #6C7A8C;
        selection-color: {SECONDARY_COLOR};
    }}
    QHeaderView::section {{
        background-color: {SECONDARY_COLOR};
        color: {MAIN_COLOR};
        font-weight: bold;
        font-family: Didot;
        font-size: 16px;
        padding: 8px;
        border: 1px solid {MAIN_COLOR};
    }}
    QTableWidget::item {{
        border: 1px solid #D3D3D3;
        padding: 6px;
        font-family: Didot;
    }}
    QTableCornerButton::section {{
        background-color: {SECONDARY_COLOR};
        border: 1px solid {MAIN_COLOR};
    }}
"""


class Ui_MainWindow(object):
    """
    This class sets up the main window UI components with reusable helpers.
    All QGroupBox, QPushButton, and QLabel objects are stored as self.<variable_name>
    so you can access them in other files or code sections.
    """

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(WINDOW_STYLE)
        MainWindow.setWindowTitle("MainWindow")  # Set title directly

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ------------------ Title Bar ------------------ #
        self.setup_title_bar()

        # ------------------ Side Bar ------------------- #
        self.setup_side_bar()

        # ------------------ Recognized Song Data ------- #
        self.setup_recognized_song_data()

        # ------------------ Recognize Song Bar --------- #
        self.setup_recognize_song_bar()

        # ------------------ Spectrogram Group Box ------ #
        self.setup_table_index_group()

        # ------------------ Quit Button ---------------- #
        self.setup_quit_button()

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ------------------------------------------------------------------------
    #                           UTILITY METHODS
    # ------------------------------------------------------------------------
    def create_label(self, parent, text="", geometry=None, max_size=None, font=None, style_sheet="", alignment=None):
        """
        Utility to create a QLabel, assign it as self.<var_name>,
        and set the text/styles directly.
        """
        label = QtWidgets.QLabel(parent)
        label.setText(text)

        if geometry is not None:
            label.setGeometry(geometry)
        if max_size is not None:
            label.setMaximumSize(max_size)
        if font is not None:
            label.setFont(font)
        if style_sheet:
            label.setStyleSheet(style_sheet)
        if alignment is not None:
            label.setAlignment(alignment)

        return label

    def create_button(self, parent, text="", geometry=None, max_size=None, font=None, style_sheet="", cursor=None):
        """
        Utility to create a QPushButton, assign it as self.<var_name>,
        and set the text/styles directly.
        """
        button = QtWidgets.QPushButton(parent)
        button.setText(text)

        if geometry is not None:
            button.setGeometry(geometry)
        if max_size is not None:
            button.setMaximumSize(max_size)
        if font is not None:
            button.setFont(font)
        if style_sheet:
            button.setStyleSheet(style_sheet)
        if cursor is not None:
            button.setCursor(cursor)

        return button

    def create_slider(self, parent, orientation=QtCore.Qt.Horizontal, method=None):
        slider = QtWidgets.QSlider(orientation, parent)

        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        slider.setStyleSheet(SLIDER_STYLESHEET)
        if method:
            slider.valueChanged.connect(method)

        return slider

    def create_graph(self, group_box):
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground(f'{MAIN_COLOR}')

        graph_layout = QtWidgets.QVBoxLayout()
        graph_layout.addWidget(plot_widget)
        group_box.setLayout(graph_layout)

        # Configure plot item within the widget
        plot_item = plot_widget.getPlotItem()
        plot_item.hideButtons()
        # plot_item.getViewBox().setMouseEnabled(x=False, y=False)
        plot_item.getAxis('left').setLabel('Frequency (Hz)')
        plot_item.getAxis('bottom').setLabel('Time (s)')

        return plot_widget

    def create_table(self, group_box):
        table_widget = QtWidgets.QTableWidget()
        table_widget.setColumnCount(4)  # Number of columns
        table_widget.setHorizontalHeaderLabels([
            "Song Name", "Similarity Index (%)", "Song Type", "Match Status"
        ])

        table_widget.setStyleSheet(TABLE_STYLESHEET)
        table_widget.horizontalHeader().setStretchLastSection(True)
        table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Adjust row headers
        table_widget.verticalHeader().setVisible(True)
        table_widget.verticalHeader().setStyleSheet(f"color: {SECONDARY_COLOR}; font-size: 14px; font-family: Didot;")

        # Make cells read-only
        table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Layout for the table
        table_layout = QtWidgets.QVBoxLayout()
        table_layout.addWidget(table_widget)
        group_box.setLayout(table_layout)

        return table_widget

    # ------------------------------------------------------------------------
    #                           UI SETUP HELPERS
    # ------------------------------------------------------------------------
    def setup_title_bar(self):
        """
        Creates the top title bar with an icon and a label.
        """
        # Container
        self.layout_widget_title_bar = QtWidgets.QWidget(self.centralwidget)
        self.layout_widget_title_bar.setGeometry(QtCore.QRect(20, 0, 300, 80))
        self.layout_widget_title_bar.setObjectName("layout_widget_title_bar")

        # Horizontal Layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layout_widget_title_bar)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Icon
        self.title_icon = QtWidgets.QLabel(self.layout_widget_title_bar)
        self.title_icon.setObjectName("title_icon")
        self.title_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.title_icon.setPixmap(QtGui.QPixmap("static/images/Fingerprint.png"))
        self.title_icon.setScaledContents(True)
        self.title_icon.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addWidget(self.title_icon)

        # Label
        self.title_label = self.create_label(
            parent=self.layout_widget_title_bar,
            text="Soundprints",
            max_size=QtCore.QSize(179, 38),
            font=TITLE_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.horizontalLayout.addWidget(self.title_label)

    def setup_side_bar(self):
        """
        Creates the left side bar with different sections (song, vocals, instruments),
        plus the Generate and Cancel buttons.
        """
        self.sidebar_main_layout = QtWidgets.QWidget(self.centralwidget)
        self.sidebar_main_layout.setGeometry(QtCore.QRect(10, 80, 260, 650))
        self.sidebar_main_layout.setObjectName("sidebar_main_layout")

        self.upload_songs_layout = QtWidgets.QVBoxLayout(self.sidebar_main_layout)
        self.upload_songs_layout.setContentsMargins(0, 0, 0, 0)
        self.upload_songs_layout.setObjectName("upload_songs_layout")

        # Sidebar Title
        self.sidebar_title = self.create_label(
            parent=self.sidebar_main_layout,
            text="Weighted Blender",
            max_size=QtCore.QSize(240, 80),
            font=SIDEBAR_TITLE_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.upload_songs_layout.addWidget(self.sidebar_title)

        # ========== Upload Song 01 Song ==========
        self.uploaded_song_01_layout = QtWidgets.QVBoxLayout()
        self.uploaded_song_01_layout.setObjectName("upload_song_01_mixer")

        self.upload_song_01_label_title = self.create_label(
            parent=self.sidebar_main_layout,
            text="First Audio",
            max_size=QtCore.QSize(240, 40),
            font=SECTION_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.uploaded_song_01_layout.addWidget(self.upload_song_01_label_title)

        self.uploaded_song_01_button = self.create_button(
            parent=self.sidebar_main_layout,
            text="Upload",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.uploaded_song_01_layout.addWidget(self.uploaded_song_01_button)

        self.uploaded_song_01_name_label = self.create_label(
            parent=self.sidebar_main_layout,
            max_size=QtCore.QSize(240, 17),
            font=ITEM_NAME_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.uploaded_song_01_layout.addWidget(self.uploaded_song_01_name_label)

        self.upload_songs_layout.addLayout(self.uploaded_song_01_layout)

        # ========== Upload Song 02 Song ==========
        self.uploaded_song_02_layout = QtWidgets.QVBoxLayout()
        self.uploaded_song_02_layout.setObjectName("upload_song_02_mixer")

        self.upload_song_02_label_title = self.create_label(
            parent=self.sidebar_main_layout,
            text="Second Audio",
            max_size=QtCore.QSize(240, 40),
            font=SECTION_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.uploaded_song_02_layout.addWidget(self.upload_song_02_label_title)

        self.uploaded_song_02_button = self.create_button(
            parent=self.sidebar_main_layout,
            text="Upload",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.uploaded_song_02_layout.addWidget(self.uploaded_song_02_button)

        self.uploaded_song_02_name_label = self.create_label(
            parent=self.sidebar_main_layout,
            max_size=QtCore.QSize(240, 17),
            font=ITEM_NAME_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.uploaded_song_02_layout.addWidget(self.uploaded_song_02_name_label)

        self.upload_songs_layout.addLayout(self.uploaded_song_02_layout)

        # ========== Songs Weight ==========
        self.songs_weight_layout = QtWidgets.QVBoxLayout()
        self.songs_weight_layout.setObjectName("songs_weight_layout")

        self.songs_weight_slider_label = self.create_label(
            parent=self.sidebar_main_layout,
            text="Song 1:    50%    -   Song 2:     50%",
            max_size=QtCore.QSize(240, 17),
            font=ITEM_NAME_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.songs_weight_layout.addWidget(self.songs_weight_slider_label)

        self.songs_weight_slider = self.create_slider(
            parent=self.sidebar_main_layout
        )
        self.songs_weight_layout.addWidget(self.songs_weight_slider)

        self.upload_songs_layout.addLayout(self.songs_weight_layout)

        # ========== Generate & Cancel ==========

        self.reset_button = self.create_button(
            parent=self.sidebar_main_layout,
            text="Reset",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )

        self.upload_songs_layout.addWidget(self.reset_button)

    def setup_recognize_song_bar(self):
        """
        Creates the horizontal layout to let users choose an unknown song to recognize.
        """
        self.recognized_song_layout = QtWidgets.QWidget(self.centralwidget)
        self.recognized_song_layout.setGeometry(QtCore.QRect(550, 0, 450, 90))
        self.recognized_song_layout.setObjectName("recognized_song_layout")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.recognized_song_layout)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.recognize_song_label = self.create_label(
            parent=self.recognized_song_layout,
            text="Choose Unknown Audio",
            max_size=QtCore.QSize(240, 40),
            font=SECTION_FONT,
            style_sheet=LABEL_WHITE_TEXT
        )
        self.horizontalLayout_2.addWidget(self.recognize_song_label)

        self.recognize_song_button = self.create_button(
            parent=self.recognized_song_layout,
            text="Upload Song",
            max_size=QtCore.QSize(240, 40),
            style_sheet=BUTTON_STYLE,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
        self.horizontalLayout_2.addWidget(self.recognize_song_button)

    def setup_table_index_group(self):
        """
        Group box for displaying the recognized song’s similarity index in a table.
        """
        self.recognized_song_index_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.recognized_song_index_groupBox.setGeometry(QtCore.QRect(280, 90, 981, 541))
        self.recognized_song_index_groupBox.setFont(QtGui.QFont("Didot"))
        self.recognized_song_index_groupBox.setStyleSheet(LABEL_WHITE_TEXT)
        self.recognized_song_index_groupBox.setObjectName("recognized_song_index_groupBox")
        self.recognized_song_index_groupBox.setTitle("Similarity Index")  # GroupBox title set directly

        self.table_widget = self.create_table(self.recognized_song_index_groupBox)

    def setup_recognized_song_data(self):
        self.recognized_song_data_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.recognized_song_data_groupBox.setGeometry(QtCore.QRect(480, 640, 400, 120))
        self.recognized_song_data_groupBox.setFont(QtGui.QFont("Didot"))
        self.recognized_song_data_groupBox.setStyleSheet(GROUPBOX_WHITE_TEXT)
        self.recognized_song_data_groupBox.setObjectName("recognized_song_data_groupBox")
        self.recognized_song_data_groupBox.setTitle("Recognized Song")  # GroupBox title set directly

        # Title label inside groupbox
        self.recognized_song_label = self.create_label(
            parent=self.recognized_song_data_groupBox,
            geometry=QtCore.QRect(40, 30, 270, 70),
            max_size=QtCore.QSize(300, 80),
            font=SIDEBAR_TITLE_FONT,
            style_sheet=f"color:{SECONDARY_COLOR}; background-color:none;"
        )

        # Icon inside groupbox
        self.recognized_song_icon = QtWidgets.QLabel(self.recognized_song_data_groupBox)
        self.recognized_song_icon.setObjectName("recognized_song_icon")
        self.recognized_song_icon.setGeometry(QtCore.QRect(300, 30, 80, 79))
        self.recognized_song_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.recognized_song_icon.setStyleSheet("background-color:none")
        # self.recognized_song_icon.setPixmap(QtGui.QPixmap("static/images/pinkfloyd.png"))
        self.recognized_song_icon.setScaledContents(True)
        self.recognized_song_icon.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)

    def setup_quit_button(self):
        """
        Creates the quit button at the top-right corner of the window.
        """
        self.quit_app_button = self.create_button(
            parent=self.centralwidget,
            text="X",
            geometry=QtCore.QRect(1200, 18, 50, 50),
            max_size=QtCore.QSize(50, 50),
            style_sheet="""
                QPushButton { 
                    color: rgb(255, 255, 255); 
                    border: 3px solid rgb(255, 255, 255);
                }
                QPushButton:hover { 
                    border-color: rgb(253, 94, 80); 
                    color: rgb(253, 94, 80); 
                }
            """,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            font=QtGui.QFont("Hiragino Sans GB", 40, QtGui.QFont.Bold)
        )

    # ------------------------------------------------------------------------
    #                           Actions
    # ------------------------------------------------------------------------

    def add_row_to_index_table(self, song_name, similarity_index, song_type):
        new_row_index = self.table_widget.rowCount()

        # Format similarity index to remove decimals
        similarity_value = float(similarity_index.strip('%'))  # Convert '80%' to 80.0
        similarity_index = f"{int(similarity_value)}%"  # Remove decimals

        # Determine match status
        if similarity_value >= 80:
            match_status = "High"
        elif 50 <= similarity_value < 80:
            match_status = "Moderate"
        else:
            match_status = "Low"

        # Replace underscores with spaces in song name
        song_name = song_name.replace("_", " ")

        self.table_widget.insertRow(new_row_index)
        self.table_widget.setItem(new_row_index, 0, QtWidgets.QTableWidgetItem(song_name))
        self.table_widget.setItem(new_row_index, 1, QtWidgets.QTableWidgetItem(similarity_index))
        self.table_widget.setItem(new_row_index, 2, QtWidgets.QTableWidgetItem(song_type))
        self.table_widget.setItem(new_row_index, 3, QtWidgets.QTableWidgetItem(match_status))

    def clear_index_table_data(self):
        self.table_widget.setRowCount(0)

    def update_song_weight_slider_label(self):
        value = self.songs_weight_slider.value()
        self.songs_weight_slider_label.setText(f"Song 1:    {value}%    -   Song 2:     {100 - value}%")

    def update_recognized_song_data(self, title):
        try:
            image_path = f'static/songs/{title}/image.png'
        except FileNotFoundError:
            image_path = 'static/images/default_song.png'

        self.recognized_song_icon.setPixmap(QtGui.QPixmap(image_path))

        # Adjust title and size dynamically
        title = title.replace("_", " ")
        self.recognized_song_label.setText(title)

        # Adjust group box and icon placement based on title length
        text_length = len(title)

        # Resize groupbox dynamically
        if text_length > 20:
            self.recognized_song_data_groupBox.setGeometry(QtCore.QRect(480, 640, 500, 120))
            self.recognized_song_label.setGeometry(QtCore.QRect(40, 30, 370, 70))
            self.recognized_song_icon.setGeometry(QtCore.QRect(400, 30, 80, 79))
        else:
            self.recognized_song_data_groupBox.setGeometry(QtCore.QRect(480, 640, 400, 120))
            self.recognized_song_label.setGeometry(QtCore.QRect(40, 30, 270, 70))
            self.recognized_song_icon.setGeometry(QtCore.QRect(300, 30, 80, 79))

    def update_uploaded_fisrt_song_name(self, title):
        self.uploaded_song_01_name_label.setText(title)

    def update_uploaded_second_song_name(self, title):
        self.uploaded_song_02_name_label.setText(title)

    def clear_recognized_song_data(self):
        self.recognized_song_icon.setPixmap(QtGui.QPixmap(""))
        self.recognized_song_label.setText("")
        self.update_uploaded_fisrt_song_name("")
        self.update_uploaded_second_song_name("")

        self.songs_weight_slider.setValue(50)

        self.uploaded_song_01_button.setText("Upload")
        self.uploaded_song_02_button.setText("Upload")
