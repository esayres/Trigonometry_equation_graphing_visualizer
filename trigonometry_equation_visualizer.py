# A program that visualizes the graphing processes of a Trigonometry equation
# By Elijah Sayres

# command for cmd to convert .ui to .py | pyuic6 -o (python_file_name).py (pyqt_ui_file_name).ui
# command to open designer | pyqt6-tools designer | venv\Scripts\activate.bat

import tev_main_window as Tw # the Qt Gui Window
from PyQt6 import QtWidgets as Qt
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
from fractions import Fraction




class TrigEquationWindow:  # the main trig equation window
    def __init__(self):
        self.main_win = Qt.QMainWindow()
        self.ui = Tw.Ui_Trigonometry_Equation_Visualizer()
        self.ui.setupUi(self.main_win)

        # this initializes all the main variables that will be used in graphing
        self.trigonometric_function = None
        self.Period_denominator = ''
        self.Period_Numerator = None
        self.amplitude = 1
        self.New_period = 1.0
        self.phase_shift = 0
        self.vertical_shift = 0
        self.full_number = 0
        self.equation_Trig_only_keywords = ["SIN", "COS", "TAN", "CSC", "SEC", "COT"]  # this is used to check what type of trig function is in the equation
        self.equation_val_ending_point = 0

        # main page functionality adding
        self.ui.TEV_plot_main_btn.clicked.connect(self.plot_button_functionality)
        self.ui.TEV_equation1_lineEdit.returnPressed.connect(self.plot_button_functionality)
        self.ui.TEV_equation2_lineEdit.returnPressed.connect(self.plot_button_functionality)
        self.ui.TEV_equation3_lineEdit.returnPressed.connect(self.plot_button_functionality)

        # help button functionality adding
        self.ui.TEV_help_btn.clicked.connect(self.help_button_functionality)
        self.ui.TEV_go_graphing_page_btn.clicked.connect(self.back_to_graphing_button_functionality)

        # Check box functionality
        self.midline_show = self.ui.TEV_midline_show_checkbox.isChecked()
        self.radians_show = self.ui.TEV_Radians_show_check_box.isChecked()
        self.all_graphs_show = self.ui.TEV_all_graphs_show_checkbox.isChecked()
        self.fix_asymptotes = self.ui.TEV_fix_asymptotes_checkbox.isChecked()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas)

        # this changes the color and style of the graphing tool bar
        self.toolbar.setStyleSheet("/*Main Navagation Toolbar Stuff */\n"
        "background-color: #6C84E8;\n"
        "color: black;\n"
        "\n"
        "/*Font Stuff */\n"
        "font-weight: 1000px;\n"
        "font-size: 18px;\n"
        "font-family: Verdana;\n"
        "\n"
        "/*Border Stuff */\n"
        "border: 2px solid rgb(33, 37, 43);\n"
        "border-radius: 10px;")

        self.ui.verticalLayout.addWidget(self.toolbar)
        self.ui.verticalLayout.addWidget(self.canvas)


    # these 2 functions change the page when going from help and graphing
    def help_button_functionality(self):
        self.ui.TEV_stackedWidget.setCurrentWidget(self.ui.TEV_help_page)

    def back_to_graphing_button_functionality(self):
        self.ui.TEV_stackedWidget.setCurrentWidget(self.ui.TEV_Main_page)



    # this is the selection for when your trying to change from multi equation adding or single equation adding
    def Radio_buttons_functionality(self):
        if self.ui.TEV_multiply_Radiobutton.isChecked():
            different_equations_grapher = 1
        elif self.ui.TEV_Divide_Radiobutton.isChecked():
            different_equations_grapher = 2
        elif self.ui.TEV_add_Radiobutton.isChecked():
            different_equations_grapher = 3
        elif self.ui.TEV_subtract_Radiobutton.isChecked():
            different_equations_grapher = 4
        elif self.ui.TEV_solo_graphing_Radiobutton.isChecked():
            different_equations_grapher = 0
        else:
            different_equations_grapher = 0

        return different_equations_grapher


    # clears the graph and helps with readability a little
    def graph_clear(self):
        self.figure.clear()


    # checks the if the trig function is a reciprocal then converts it into its normal trig function to be divided by 1
    def trig_reciprocal_check(self, Trig_function):
        reciprocal_trig_func = Trig_function
        is_a_reciprocal = False

        if Trig_function.upper() == "CSC":
            reciprocal_trig_func = "SIN"
            is_a_reciprocal = True
        if Trig_function.upper() == "SEC":
            reciprocal_trig_func = "COS"
            is_a_reciprocal = True
        if Trig_function.upper() == "COT":
            reciprocal_trig_func = "TAN"
            is_a_reciprocal = True
        return reciprocal_trig_func, is_a_reciprocal


    # the main functionality when you click the plot button
    def plot_button_functionality(self):
        self.graph_clear()

        # this finds out what radio button you selected
        radio_options_choice = self.Radio_buttons_functionality()

        # Check box functionality
        self.midline_show = self.ui.TEV_midline_show_checkbox.isChecked()
        self.radians_show = self.ui.TEV_Radians_show_check_box.isChecked()
        self.all_graphs_show = self.ui.TEV_all_graphs_show_checkbox.isChecked()
        self.fix_asymptotes = self.ui.TEV_fix_asymptotes_checkbox.isChecked()

        # converts the line edit into a string and then removes any spaces and removes any word "pi" and replaces it with the symbol
        self.tev_equation1_text = self.ui.TEV_equation1_lineEdit.text()
        self.tev_equation2_text = self.ui.TEV_equation2_lineEdit.text()
        self.tev_equation3_text = self.ui.TEV_equation3_lineEdit.text()

        self.tev_equation1_text = str(self.tev_equation1_text).replace(' ', "")
        self.tev_equation2_text = str(self.tev_equation2_text).replace(' ', "")
        self.tev_equation3_text = str(self.tev_equation3_text).replace(' ', "")

        self.tev_equation1_text = self.tev_equation1_text.replace("pi", "π")
        self.tev_equation2_text = self.tev_equation2_text.replace("pi", "π")
        self.tev_equation3_text = self.tev_equation3_text.replace("pi", "π")

        # info GATHERING PUTTING INTO LISTS

        x, y, x2, y2, x3, y3 = 0, None, 0, None, 0, None
        recip1,recip2,recip3 = False, False, False
        vert_shift1, vert_shift2, vert_shift3 = 0, 0, 0  # the midlines of all equations
        trigfunc1, trigfunc2, trigfunc3 = "None", "None", "None" # trigfunc will eventually hold what type of function the equation is to then be used in plotting
        La1, La2, La3 = None, None, None # La is just a abbreviation of Leftside_equationAmplitude
        self.Leftside_equationAmplitude = None # a leftside_equation is just anything on the left side of a equation that looks like this 513 = sin(x) (513 is the leftside)


        if self.equation_checker(self.tev_equation1_text) is False: # PREVENTS RANDOM INVALID CHECKS
            self.trigonometric_function, self.amplitude = self.invalid_trig_function(self.trigonometric_function, self.amplitude)
            self.trigonometric_function, reciprocal_check = self.trig_reciprocal_check(self.trigonometric_function)
            x, y, trigfunc1, recip1 = self.y_equation_grabber(self.amplitude, self.trigonometric_function, self.vertical_shift, self.New_period, self.Period_Numerator, self.Period_denominator, self.phase_shift, reciprocal_check)
            vert_shift1 = self.vertical_shift
            # checks if there is a number on the far leftside (64 = sinx) checks for the 64 and if not returns None
            if self.Leftside_equationAmplitude != None:
                La1 = self.Leftside_equationAmplitude
            else:
                La1 = None

        if self.equation_checker(self.tev_equation2_text) is False: # PREVENTS RANDOM INVALID CHECKS
            self.trigonometric_function, self.amplitude = self.invalid_trig_function(self.trigonometric_function, self.amplitude)
            self.trigonometric_function, reciprocal_check = self.trig_reciprocal_check(self.trigonometric_function)
            x2, y2, trigfunc2, recip2 = self.y_equation_grabber(self.amplitude, self.trigonometric_function, self.vertical_shift, self.New_period, self.Period_Numerator, self.Period_denominator, self.phase_shift, reciprocal_check)
            vert_shift2 = self.vertical_shift
            # checks if there is a number on the far leftside (64 = sinx) checks for the 64 and if not returns None
            if self.Leftside_equationAmplitude != None:
                La2 = self.Leftside_equationAmplitude
            else:
                La2 = None

        if self.equation_checker(self.tev_equation3_text) is False: # PREVENTS RANDOM INVALID CHECKS
            self.trigonometric_function, self.amplitude = self.invalid_trig_function(self.trigonometric_function, self.amplitude)
            self.trigonometric_function, reciprocal_check = self.trig_reciprocal_check(self.trigonometric_function)
            x3, y3, trigfunc3,recip3 = self.y_equation_grabber(self.amplitude, self.trigonometric_function, self.vertical_shift, self.New_period, self.Period_Numerator, self.Period_denominator, self.phase_shift, reciprocal_check)
            vert_shift3 = self.vertical_shift
            # checks if there is a number on the far leftside (64 = sinx) checks for the 64 and if not returns None
            if self.Leftside_equationAmplitude != None:
                La3 = self.Leftside_equationAmplitude
            else:
                La3 = None

        # this is a just in case if period somehow gets returned 0 it will make sure it turns into a 1
        # im 99% sure that this isnt needed but just in case
        if self.New_period == 0:
            self.New_period = 1

        # this is the main plotting function that graphs all the sine functions/equations
        self.plot_all(self.New_period, self.radians_show, x, y, x2, y2, x3, y3, trigfunc1, trigfunc2, trigfunc3, La1, La2, La3,
                      vert_shift1, vert_shift2, vert_shift3, self.midline_show, radio_options_choice, self.all_graphs_show, self.fix_asymptotes,recip1,recip2,recip3)



    # if an invalid function is given for example just numbers (2) this will convert that into a valid trig function 0*sin(0) which ends up = 0 so it doesn't graph anything
    def invalid_trig_function(self, Trig_function, amplitude):
        trig_func = Trig_function
        new_amplitude = amplitude
        if Trig_function == "None":
            trig_func = "SIN"
            new_amplitude = 0
        return trig_func, new_amplitude


    # the function that attempts to gather a midline of the graph for use
    def multi_equation_midline_calcuation(self, vert_shift1, vert_shift2, vert_shift3):
        Dvert_shift1 = vert_shift1
        Dvert_shift2 = vert_shift2
        Dvert_shift3 = vert_shift3

        if vert_shift1 == 0:
            Dvert_shift1 = 0
        if vert_shift2 == 0:
            Dvert_shift2 = 0
        if vert_shift3 == 0:
            Dvert_shift3 = 0

        if vert_shift1 == 0 and vert_shift2 == 0 or vert_shift2 == 0 and vert_shift3 == 0 or vert_shift3 == 0 and vert_shift1 == 0:
            multi_equation_midline = Dvert_shift1 + Dvert_shift2 + Dvert_shift3
        else:
            multi_equation_midline = (Dvert_shift1 + Dvert_shift2 + Dvert_shift3) / 2
        return multi_equation_midline



    # plot all creates complies the equation that was given and then plots it to the graph
    def plot_all(self, Period, Radian_or_no_radians, x1, y1, x2, y2, x3, y3, trigfunc1, trigfunc2, trigfunc3, la1, la2, la3, vert_shift1,
                 vert_shift2, vert_shift3, midline_shower, radio_button_type, all_graphs_shower, attempt_asymptotes_fix,recip1,recip2,recip3):

        # this initializes the plotting figure/graph
        axes = self.figure.add_subplot(111)
        x_limits = 10 * np.pi


        # this converts all the points into radians and creates a label for them on graph
        if Radian_or_no_radians is True:
            radians, radians_labels = self.radians_label_maker()
            axes.set_xticks(ticks=radians, labels=radians_labels)

        # this checks if the sine function is tan then plots it differently because tan just works alittle differently and needs to
        if radio_button_type == 0 or all_graphs_shower is True:
            ny1 = y1
            ny2 = y2
            ny3 = y3
            if y1 is None:
                ny1 = 0
            if y2 is None:
                ny2 = 0
            if y3 is None:
                ny3 = 0

            # how the function graphs Tan
            if trigfunc1.upper() == "TAN" or recip1 is True:
                x = np.linspace(-2 * np.pi, 20 * np.pi, 1000)
                if attempt_asymptotes_fix is True:
                    ny1[np.abs(np.cos(x)) <= np.abs(np.sin(x[1] - x[0]))] = np.nan


                axes.set_ylim(-1.5, 1.5)
                axes.plot(x, ny1, color="#6BAD44") # green
            # how the function graphs Sin / Cos
            else:
                axes.plot(x1, ny1, color="#6BAD44")  # green

            # how the function graphs Tan
            if trigfunc2.upper() == "TAN" or recip2 is True:
                x = np.linspace(-2 * np.pi, 20 * np.pi, 1000)
                if attempt_asymptotes_fix is True:
                    ny2[np.abs(np.cos(x)) <= np.abs(np.sin(x[1] - x[0]))] = np.nan


                axes.set_ylim(-1.5, 1.5)
                axes.plot(x, ny2, color="#55C4C4") # blue
            # how the function graphs Sin / Cos
            else:
                axes.plot(x2, ny2, color="#55C4C4") # blue

            # how the function graphs Tan
            if trigfunc3.upper() == "TAN" or recip3 is True:
                x = np.linspace(-2 * np.pi, 20 * np.pi, 1000)
                if attempt_asymptotes_fix is True:
                    ny3[np.abs(np.cos(x)) <= np.abs(np.sin(x[1] - x[0]))] = np.nan


                axes.set_ylim(-1.5, 1.5)
                axes.plot(x, ny3, color="#F66545")  # red
            # how the function graphs Sin / Cos
            else:
                axes.plot(x3, ny3, color="#F66545")  # red


            if vert_shift1 is not None and midline_shower is True:
                axes.axhline(vert_shift1, color="#6BAD44", linestyle="-.")  # this shows off the midline of the graph

            if vert_shift2 is not None and midline_shower is True:
                axes.axhline(vert_shift2, color="#55C4C4", linestyle="-.")  # this shows off the midline of the graph

            if vert_shift3 is not None and midline_shower is True:
                axes.axhline(vert_shift3, color="#F66545", linestyle="-.")  # this shows off the midline of the graph

        # multiple Equation plotting
        if 1 <= radio_button_type <= 4:
            ny1 = y1
            ny2 = y2
            ny3 = y3
            multi_equation_Y = 0
            nx = np.linspace(-2 * np.pi, 20 * np.pi, 1000)
            # this fixes a crash if you don't input an equation into one of the slots
            if y1 is None:
                if 1 <= radio_button_type <= 2:
                    ny1 = 1
                else:
                    ny1 = 0
            if y2 is None:
                if 1 <= radio_button_type <= 2:
                    ny2 = 1
                else:
                    ny2 = 0
            if y3 is None:
                if 1 <= radio_button_type <= 2:
                    ny3 = 1
                else:
                    ny3 = 0

            # this does the math that gets the multi equation graph
            if radio_button_type == 1: # mult
                multi_equation_Y = ny1 * ny2 * ny3
            elif radio_button_type == 2: #divide
                multi_equation_Y = ny1 / ny2 / ny3
            elif radio_button_type == 3: # add
                multi_equation_Y = ny1 + ny2 + ny3
            elif radio_button_type == 4: # subtract
                multi_equation_Y = ny1 - ny2 - ny3

            # this attempts to fix the connecting vertical asymptotes that happen when graphing with tan
            if trigfunc1 == "TAN" or trigfunc2 == "TAN" or trigfunc3 == "TAN" or recip1 is True or recip2 is True or recip3 is True:
                axes.set_ylim(-1.5, 1.5)
                if attempt_asymptotes_fix is True:
                    multi_equation_Y[np.abs(np.cos(nx)) <= np.abs(np.sin(nx[1] - nx[0]))] = np.nan

            # this attempts to show a midline of the multi_equation line when it can
            if midline_shower is True:
                multi_equation_midline = self.multi_equation_midline_calcuation(vert_shift1, vert_shift2, vert_shift3)
                axes.axhline(multi_equation_midline, color="purple", linestyle="-.") # multi- midline

            # this graphs the multi-equation graph
            try:
                axes.plot(nx, multi_equation_Y, color="purple")
            except ValueError:
                multi_equation_Y = 0*np.sin(0*nx)
                axes.plot(nx, multi_equation_Y, color="purple")

        # this colors the lines when using the = equations like [2 = sin(x)]
        if la1 is not None:
            axes.axhline(la1, color="#6BAD44", linestyle="--")
        if la2 is not None:
            axes.axhline(la2, color="#55C4C4", linestyle="--")
        if la3 is not None:
            axes.axhline(la3, color="#F66545", linestyle="--")

        # turns on the graph when ploting Tan or reciprocals
        if trigfunc1 == "TAN" or trigfunc2 == "TAN" or trigfunc3 == "TAN" or recip1 is True or recip2 is True or recip3 is True:
            axes.grid()

        # this draws the x and y line and also updates the graw when you plot to it
        axes.set_xlim(-0.02, x_limits / Period * .5) # this forces the graph to show only a small amount of it at the start
        axes.axhline(color="black")
        axes.axvline(color="black")
        self.canvas.draw()


    # this compiles the equations that is gets from the inputs an then turns it into a Y value so it can be plotted
    def y_equation_grabber(self, Amplitude, Trig_function, Vertical_shift, Period, Period_numerator, Period_denominator, Phase_shift, is_it_reciprocal):
        x = np.linspace(-2 * np.pi, 20 * np.pi, 1000)

        # this trigfunc turns what ever trig_function it is into a np.trig_function like (np.sin) or (np.cos)
        trigfunc = getattr(np, Trig_function.lower())
        if is_it_reciprocal is True:
            # this handles if the function is a reciprocal or not
            if Period_denominator == "":
                y = 1 / (Amplitude * trigfunc(Period * (x + Phase_shift)) + Vertical_shift)
            else:
                y = 1 / (Amplitude * trigfunc(Period_numerator / Period_denominator * (x + Phase_shift)) + Vertical_shift)
        else:
            if Period_denominator == "":
                y = Amplitude * trigfunc(Period * (x + Phase_shift)) + Vertical_shift
            else:
                y = Amplitude * trigfunc(Period_numerator / Period_denominator * (x + Phase_shift)) + Vertical_shift
        return x, y, Trig_function, is_it_reciprocal


    def radians_label_maker(self):
        radian_mult = np.arange(-4, 41, 2) / 2
        extra_points = np.arange(1, 41) / 2
        radians = np.concatenate((radian_mult * np.pi, extra_points * np.pi))
        all_points = np.concatenate((radian_mult, extra_points))
        radians_labels = []  # a empty list that will start to contain all of the radians label

        # this for loop puts all the points that will be the labels on graph into the list then it sets the Xpoint labels
        for n in all_points:
            if n.is_integer():
                radians_labels.append(f'${int(n)}\\pi$')
            else:
                # this converts any decimals to a fraction then it puts the numerator into the top Radians Labels to be shown on graph
                fraction = Fraction(n).limit_denominator()
                fraction_num = fraction.numerator
                if fraction.numerator == 1:
                    fraction_num = ''
                radians_labels.append(f'${fraction_num}\\pi$/2')
        return radians, radians_labels


    ############################
    #
    # PARSING THE EQUATIONS
    #
    ############################


    # this grabs the maximum amount of numbers in the amplitude, and then it skips over decimals, fraction marks, and pi symbols
    def Amplitude_number_length_grabber(self, equation, starting_point):
        val_ending_point = 0
        if equation[starting_point] == "-":
            starting_point += 1
            Leftside_equation_amp_is_negative = True
        else:
            Leftside_equation_amp_is_negative = False
        for val in range(starting_point, len(equation)):
            if not equation[val].isdigit() and equation[val] != "." and equation[val] != "/" and equation[val] != 'π':
                val_ending_point = val
                break
        return val_ending_point, Leftside_equation_amp_is_negative


    # This goes through the entire equation provided then converts it into something that y_equation_grabber can use to create y values
    def equation_checker(self, equation):
        # this resets all of the variables so previous graphs doesn't break the system
        Amplitude_is_negative = False
        self.trigonometric_function = None
        self.amplitude = 1
        self.phase_shift = 0
        self.vertical_shift = 0
        self.New_period = 1.0
        self.Leftside_equationAmplitude = None

        try:
            # this check if the equation starts on a number, a negative sugn, or on pi
            if equation[0].isdigit() or equation[0] == "-" or equation[0] == "π":

                # this checks if its negative or not
                if equation[0] == "-":
                    Amplitude_is_negative = True
                    self.equation_val_ending_point, doesnt_matter = self.Amplitude_number_length_grabber(equation, 1)
                    amplitude_equation = equation[1: self.equation_val_ending_point]

                else:
                    self.equation_val_ending_point, doesnt_matter = self.Amplitude_number_length_grabber(equation, 0)
                    amplitude_equation = equation[0: self.equation_val_ending_point]

                # if the equation doesnt look like 3= sinx then it will grab the amplitude normally
                try:
                    if equation[self.equation_val_ending_point] != "=":
                        self.amplitude = self.phase_vertical_shifts_and_period_radians_checker(amplitude_equation,1)
                        if Amplitude_is_negative is True:
                            self.amplitude *= -1
                except ValueError:
                    return 0


                # this checks if the equation has a = sign after the number and will convert it to something that can be graphed
                if equation[self.equation_val_ending_point] == "=":
                    # this takes the far left side equation number and puts it into a variable called leftside_equation (also checks if negative and then makes it negative)
                    if Amplitude_is_negative is False:
                        left_side_equation = equation[0: self.equation_val_ending_point]
                        self.Leftside_equationAmplitude = self.phase_vertical_shifts_and_period_radians_checker(left_side_equation, 1)

                    else:
                        left_side_equation = equation[1: self.equation_val_ending_point]
                        self.Leftside_equationAmplitude = self.phase_vertical_shifts_and_period_radians_checker(left_side_equation, 1)
                        self.Leftside_equationAmplitude = -1 * self.Leftside_equationAmplitude

                    self.equation_val_ending_point += 1
                    # this checks the equation for an ending point after the "=" then it puts it into 2 variables called Leftequation_val_point
                    # which is the new farthest point (trigfunc). the next variable just checks if the equation is negative or not and skips then forces it to be negative
                    if equation[self.equation_val_ending_point].isdigit() or equation[self.equation_val_ending_point] == "-":
                        self.LEFTequation_val_ending_point, Leftside_equation_amp_is_negative = self.Amplitude_number_length_grabber(equation, self.equation_val_ending_point)

                        if Leftside_equation_amp_is_negative is True:
                            if equation[self.LEFTequation_val_ending_point].isdigit():
                                self.LEFTequation_val_ending_point += 1
                        # the grabs the real amplitude of the equation and checks if its negative or not
                        left_side_equation = equation[self.equation_val_ending_point: self.LEFTequation_val_ending_point + 1]
                        self.amplitude = self.phase_vertical_shifts_and_period_radians_checker(left_side_equation, 1)

                        if Leftside_equation_amp_is_negative is True:
                            self.amplitude *= -1

                        # this then forces the main ending point to be after the amplitude so it works the same with rest of the parser
                        self.equation_val_ending_point = self.LEFTequation_val_ending_point

                    # then this starts the rest of the equation parsing after the amplitude is grabbed
                    self.Sinusoidal_form_checker(equation)
                    return False

                # this checks if the equation is in the form of Asin(k(x-b))+C
                else:
                    self.Sinusoidal_form_checker(equation)
                    return False
            # this checks if the equation is either in the form of sin(k(x-b))+C
            else:
                # checks if equation the equation is valid or not and returns True meaning it is invalid and will be handled after equation checker
                if self.trigonometric_function is None:
                    self.trigonometric_function = "None"
                    self.amplitude = 1
                    self.equation_val_ending_point = 0
                    if self.Sinusoidal_form_checker(equation) is True:  # this returns if it detects that it's not a valid expression
                        return True
                    return False
        except IndexError:
            pass



    # this handles the rest of the parsing after equation checker gets the amplitude
    def Sinusoidal_form_checker(self, equation):

        # this sets the ending point to after the trigonmetric word and then checks for what type of trig function it is (sin,cos,etc..)
        symbol_check = self.equation_val_ending_point + 3
        for word in self.equation_Trig_only_keywords:
            if equation[self.equation_val_ending_point: symbol_check].upper() == word:
                self.trigonometric_function = word
                # this checks if the equation looks like sinx
                if equation[symbol_check].upper() == "X":
                    self.vertical_shift = self.Vertical_shift_checker(equation, symbol_check + 1)


                # this checks if the equation looks like sin(x)
                elif equation[symbol_check].upper() == "(":
                    if equation[symbol_check + 1].upper() == "X": # this == sin(x or sinx
                        if equation[symbol_check + 2].upper() == ")": # this == if sin(x)
                            self.vertical_shift = self.Vertical_shift_checker(equation, symbol_check + 3)


                        else:
                            self.phase_shift, ending_point = self.phase_shift_checker(equation, symbol_check + 2)
                            self.vertical_shift = self.Vertical_shift_checker(equation, ending_point)


                    else:
                        self.New_period, self.Period_Numerator, self.Period_denominator, X_point = self.period_finder_and_checker(equation, symbol_check + 1)
                        self.phase_shift, ending_point = self.phase_shift_checker(equation, X_point)
                        self.vertical_shift = self.Vertical_shift_checker(equation, ending_point)

                else:
                    self.New_period, self.Period_Numerator, self.Period_denominator, X_point= self.period_finder_and_checker(equation, symbol_check)
                    self.vertical_shift = self.Vertical_shift_checker(equation, X_point)

        if self.trigonometric_function is None:
            self.trigonometric_function = "None"
            return True


    # This is the main radian checker for the entire equation (it doesn't just check phase/vertical/and period) it checks everything
    # it's probably slightly missed named
    def phase_vertical_shifts_and_period_radians_checker(self, compiled_equation, type_of_check):
        side_number2 = 0
        shift_denominator = ''
        shift_numerator = None

        # first it checks if for a pi symbol or a fraction mark "/" if it finds those it will break and handle it correctly
        Shift, pi_encountered, shift_is_fraction, ending_point = self.decimal_finder(compiled_equation, 0)
        # if it finds pi it will multiply the number by itself
        if pi_encountered is True:
            Shift *= 3.14159
            ending_point += 1
            # this while loop checks for numbers or pi on the right side of it for example (pi*2) or (pi*pi/2)
            while True:
                side_number, pi_encountered, shift_is_fraction, ending_point = self.decimal_finder(compiled_equation, ending_point)
                if pi_encountered is True:
                    side_number *= 3.14159
                    side_number2 = side_number
                    ending_point += 1
                else:
                    Shift *= side_number
                    ending_point += 1
                    break
            Shift += side_number2

        # if the shift/equation its checking is a fraction then this will compile the into a decimal (even if radians are)
        # this basically does the same thing from upabove but splits the whole equation into 2 variables (numerator and denominator)
        if shift_is_fraction is True:
            side_number2 = 1
            ending_point += 1
            shift_numerator = Shift
            new_ending_point = ending_point
            while True:
                side_number, pi_encountered, shift_is_fraction, ending_point = self.decimal_finder(compiled_equation, new_ending_point)
                if pi_encountered is True:
                    side_number *= 3.14159
                    side_number2 = side_number
                    new_ending_point += 1
                    # if this breaks ending_point += 1  was here
                else:
                    Shift = side_number * side_number2
                    side_number2 = 0
                    # if this breaks ending_point += 1  was here
                    break
            Shift += side_number2
            shift_denominator = Shift

        # when i first set of how period is graphed i used a different system that didnt support for radians,decimals. and it made use of
        # 2 different variables to calculate fractions so i just made this to prevent rewritting and possibly breaking code
        if type_of_check == 2:
            return Shift, shift_numerator, shift_denominator
        else:
            if shift_denominator != "":
                Shift = (shift_numerator / shift_denominator)
            return Shift



    # this is the first part of the Phase shift chcker where it complies the phase shift of the equation into a smaller independant equation to
    # then get sent and checked for radians and for decimals,fractions
    def phase_shift_checker(self, equation, starting_pos):
        self.full_number = 0
        try:
            if equation[starting_pos] == "-" or equation[starting_pos] == "+":
                pass
        except IndexError:
            return 0
        # checks if the Phase shift sign is positve or negative
        if equation[starting_pos] == "-":
            number_is_negative = True
        else:
            number_is_negative = False
        full_number = 0

        # this grabs the full index length of the Phase shift
        for val in range(starting_pos + 1, len(equation)):
            if equation[val].isdigit() or equation[val] == "." or equation[val] == "/" or equation[val] == "π":
                full_number = val + 1
            elif equation[val] == ")" or equation[val - 1] == ")":
                break

            else:
                break

        # this gives the complied smaller equation so it can be worked and then used to find any radians
        complied_radian_equation = equation[starting_pos + 1: full_number]
        if complied_radian_equation == "":
            number = 0
        else:
            number = self.phase_vertical_shifts_and_period_radians_checker(complied_radian_equation, 1)

        # if the phase shift is supposed to be negative it forces the number negative then returns it
        if number_is_negative is True:
            number = number * -1
        try:
            if equation[full_number + 1] == ")":
                full_number += 2
            else:
                if full_number == 0:
                    full_number = starting_pos + 1
                else:
                    full_number += 1
        except IndexError:
            if full_number == 0:
                full_number = starting_pos + 1
            else:
                full_number += 1
        return number, full_number


    # decimal finder is a main component in finding out if there is radians in the equation. what it will do is use a for loop to go through each character of the
    # complied equation then it will break once it finds a pi symbol, or a fraction then it will send it do be converted into a decimal in the end
    def decimal_finder(self, period, starting_point):
        pi_encountered = False
        period_is_fraction = False
        for val in range(starting_point, len(period)):
            if period[val].isdigit() or period[val] == ".":  # grabs parameters for full decimal number/whole number
                self.full_number = val + 1
            elif period[val] == "π":  # sets variables if pi or fraction is encountered then breaks
                pi_encountered = True
                break
            elif period[val] == "/":
                period_is_fraction = True
                break
            else:  # breaks if it encounters anything else it will brea like a "(" or "X"
                break

        # this prevents the equation from running into a value error
        try:
            number = float(period[starting_point: self.full_number])
        except ValueError:
            number = 1

        return number, pi_encountered, period_is_fraction, self.full_number



    # this basically does the same thing as the phase shift checker but its more made to fit only where period is instead
    def period_finder_and_checker(self, equation, starting_pos):
        ending_pos = 0
        period = 0
        self.full_number = 0
        for val in range(starting_pos, len(equation)):
            if equation[val].upper() == "X" or equation[val].upper() == "(":
                ending_pos = val
                period = equation[starting_pos:ending_pos]

        period = period.replace("(", "")  # gets rid of extra ( left over from the up above for loop when equation looks like sin(2(x+B))


        new_period, period_numerator, period_denominator = self.phase_vertical_shifts_and_period_radians_checker(period, 2)
        return new_period, period_numerator, period_denominator, ending_pos + 1


    # this basically does the same thing as the phase shift and period checker but its more made to fit only where vertical shift is instead
    def Vertical_shift_checker(self, equation, starting_pos):
        self.full_number = 0
        try:
            if equation[starting_pos] == "-" or equation[starting_pos] == "+" or equation[starting_pos] == ")":
                if equation[starting_pos] == ")":
                    starting_pos += 1
                pass
        except IndexError:
            return 0

        # checks if the midline/vertical shift sign is positve or negative
        if equation[starting_pos] == "-":
            number_is_negative = True
        else:
            number_is_negative = False
        full_number = 0

        # this grabs the full number of the vertical shift
        for val in range(starting_pos + 1, len(equation)):
            if equation[val].isdigit() or equation[val] == "." or equation[val] == "/" or equation[val] == "π":
                full_number = val + starting_pos + 1
            else:
                break


        complied_radian_equation = equation[starting_pos + 1: full_number]
        if complied_radian_equation == "":
            number = 0
        else:
            number = self.phase_vertical_shifts_and_period_radians_checker(complied_radian_equation, 1)

        # forces the number negative then returns it
        if number_is_negative is True:
            number = number * -1
        return number


    def show(self):
        self.main_win.show()



if __name__ == '__main__':
    # this shows full stack when errors happen
    app = Qt.QApplication(sys.argv)
    main_win = TrigEquationWindow()
    main_win.show()
    sys.exit(app.exec())