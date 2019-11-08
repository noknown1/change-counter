import tkinter as tk
from tkinter import Menu, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
import PIL.Image
import PIL.ImageTk
import numpy as np
import cv2

# DEFINITIONS #
# GUI Colors and font
WHITE = "#EEEFEA"
BLACK = "#1c1c1c"
PRIMARY = "#DCDCDC"
DEFAULT = "#F0F0F0"
FONT_PRIMARY = "Fixedsys"
FONT_SECONDARY = "System"

# INITIAL #
# Define main window
window_main = tk.Tk()
window_main.title("Change Counter")
window_main.geometry("+5+5")
window_main.resizable(False, False)
window_main.configure(bg=WHITE)

# Variables
window_main.source_image_path = ""      # Path for source image
window_main.output_image_path = ""      # Path where output image will be saved
window_main.source_image = []           # Source input image
window_main.output_image = []           # Processed output image
window_main.preview_image = []          # Preview image for GUI display
window_main.ran = False                 # Flag: True if an image has been processed, otherwise false
advanced_settings_shown = True         # Flag: True if the advanced settings panel is shown

# Processing options
resize_percentage = 0.30                # Percentage image will be scaled down to in order to increase performance
error_small = 0.04                      # Acceptable size ratio error for smaller coins
error_large = 0.10                      # Acceptable size ratio error for larger coins
d_resize_percentage = 30                # Default value
d_error_small = 4                       # Default value
d_error_large = 10                      # Default value
edge_threshold = 200                    # Specifies how sensitive the Hough transform's edge detector will be to edges
circle_threshold = 35                   # Threshold controlling how sensitive the detection of circle centers will be
d_edge_threshold = 200                  # Default value
d_circle_threshold = 35                 # Default value
blur_kernel = 15                        # Specifies kernel size for gaussian blur ran on image during pre-proccessing
d_blur_kernel = 15                      # Default value

# FUNCTION DEFINITIONS #
# process_image: processes image, counts all coins and totals their values
def process_image():
    global resize_percentage, error_small, error_large, edge_threshold, circle_threshold

    # DEFINITIONS #
    # Defined coin ratios and ranges
    DIME = 1
    PENNY = 1.064
    NICKLE = 1.184
    QUARTER = 1.355
    DIME_RANGE = (DIME - (DIME * error_small), DIME + (DIME * error_small))
    PENNY_RANGE = (PENNY - (PENNY * error_small), PENNY + (PENNY * error_small))
    NICKLE_RANGE = (NICKLE - (NICKLE * error_small), NICKLE + (NICKLE * error_small))
    QUARTER_RANGE = (QUARTER - (QUARTER * error_large), QUARTER + (QUARTER * error_large))

    # Define colors (in BGR) and font
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    # PROCESS IMAGE / FIND COINS #
    # Create a copy of the source image, and pre-process it
    input_image = cv2.imread(window_main.source_image_path, 0)
    resized_dim = (int(input_image.shape[1] * resize_percentage), int(input_image.shape[0] * resize_percentage))
    input_image = cv2.resize(input_image, resized_dim, interpolation=cv2.INTER_AREA)
    output_image = cv2.cvtColor(input_image, cv2.COLOR_GRAY2BGR)
    input_image = cv2.GaussianBlur(input_image, (blur_kernel, blur_kernel), 0)


    # Use HoughCircles from cv2 to collect all circles in the image
    circles = cv2.HoughCircles(
        image=input_image,
        method=cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=95,
        param1=edge_threshold,
        param2=circle_threshold,
        minRadius=0,
        maxRadius=0)

    # Find the size of each circle as a ratio to the smallest circle
    circle_radii = circles[..., 2]
    circle_smallest = np.min(circle_radii)
    circle_ratios = np.around(np.divide(circle_radii, circle_smallest), 3)

    # Iterate through each circle to draw and count them
    circle_count = 0
    unknown_count = 0
    dimes = 0
    pennies = 0
    nickles = 0
    quarters = 0
    for circle in circles[0, :]:

        # Get the coordinates, radius and ratio size for the current circle
        coordinates = (circle[0], circle[1])
        radius = circle[2]
        ratio_size = circle_ratios[0, circle_count]

        # Set drawn circle's color (this will only change if the coin is unrecognized)
        circle_color = GREEN

        # Figure out what coin this circle is depending on what size range it fits into
        if DIME_RANGE[0] < ratio_size < DIME_RANGE[1]:
            dimes += 1
            circle_text = "D"
        elif PENNY_RANGE[0] < ratio_size < PENNY_RANGE[1]:
            pennies += 1
            circle_text = "P"
        elif NICKLE_RANGE[0] < ratio_size < NICKLE_RANGE[1]:
            nickles += 1
            circle_text = "N"
        elif QUARTER_RANGE[0] < ratio_size < QUARTER_RANGE[1]:
            quarters += 1
            circle_text = "Q"
        else:
            circle_text = "?"
            circle_color = RED
            unknown_count += 1

        # Draw a outline of the circle, as well as text indicating where the center is
        cv2.circle(output_image, coordinates, radius, circle_color, 8)
        cv2.putText(output_image, circle_text, coordinates, FONT, 1, circle_color, 2)

        # Increment number of circles found
        circle_count += 1

    # UPDATE GUI #
    # Calculate change totals
    pennies_change = np.round(pennies * 0.01, 2)
    nickles_change = np.round(nickles * 0.05, 2)
    dimes_change = np.round(dimes * 0.10, 2)
    quarters_change = np.round(quarters * 0.25, 2)
    total_coins = pennies + nickles + dimes + quarters
    total_money = pennies_change + nickles_change + dimes_change + quarters_change

    # Place text over the image
    output_text = "Total Money: $" + str(np.round(total_money, 2))
    cv2.putText(output_image, output_text, (20, 100), FONT, 2, WHITE, 2)

    # Update the output image
    window_main.output_image = output_image

    # Update output labels
    window_main.lbl_pennies_count_num.configure(text=str(pennies))
    window_main.lbl_nickles_count_num.configure(text=str(nickles))
    window_main.lbl_dimes_count_num.configure(text=str(dimes))
    window_main.lbl_quarters_count_num.configure(text=str(quarters))
    window_main.lbl_total_count_num.configure(text=str(total_coins))

    window_main.lbl_pennies_count_cur.configure(text=str(pennies_change))
    window_main.lbl_nickles_count_cur.configure(text=str(nickles_change))
    window_main.lbl_dimes_count_cur.configure(text=str(dimes_change))
    window_main.lbl_quarters_count_cur.configure(text=str(quarters_change))
    window_main.lbl_total_count_cur.configure(text=str(np.round(total_money, 2)))

# Menu commands (used for GUI menu bar)
# load_image: Asks user to choose a source image to process
def load_image():
    # Get the image's path, then load it into the program
    window_main.source_image_path = askopenfilename(title="Load Image")
    window_main.source_image = cv2.cvtColor(cv2.imread(window_main.source_image_path), cv2.COLOR_BGR2RGB)

    # Update program status and print to console
    update_status("Loaded image " + window_main.source_image_path + ".")

    # Show the image in the preview box
    show_image(window_main.source_image)

# save_image: Allows user to save the output image to a path
def save_image():
    window_main.output_image_path = asksaveasfilename(title="Save Output Image")
    update_status("Saved output image " + window_main.output_image_path)

# Program functions (used to process the image)
# run: will process image and display it in the preview box
def run():
    global resize_percentage, error_large, error_small, edge_threshold, circle_threshold, blur_kernel
    # Make sure there is a selected image to process
    if window_main.source_image_path == "":
        update_status("No image selected. Please load an image then press run.")
        return

    # Get parameter data from sliders
    resize_percentage = window_main.slider_resize_percentage.get() * 0.01
    error_small = window_main.slider_small_error.get() * 0.01
    error_large = window_main.slider_large_error.get() * 0.01
    edge_threshold = window_main.slider_edge_threshold.get()
    circle_threshold = window_main.slider_circle_threshold.get()
    blur_kernel = window_main.slider_blur_kernel.get()

    update_status("Processing image...")
    process_image()
    update_status("Image processed, output shown.")
    window_main.ran = True
    show_output()

# Helper functions (used for misc. GUI)
# show image: will show an image in the preview box
def show_image(img):
    img_height, img_width = img.shape[:2]
    img = cv2.resize(img, (int(570 * (img_width / img_height)), 570), interpolation=cv2.INTER_AREA)
    window_main.preview_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
    window_main.image_canvas.create_image(300, 285, anchor=tk.CENTER, image=window_main.preview_image)

# show_source: shows the source image in the preview box
def show_source():
    # Make sure there is a selected image to display
    if window_main.source_image_path == "":
        update_status("No image selected. Please load an image then press run.")
        return
    show_image(window_main.source_image)

# show_output: shows the output image in the preview box
def show_output():
    # Make sure there is a selected image to display
    if window_main.ran == False:
        update_status("Run the program to see output image.")
        return
    show_image(window_main.output_image)

# update_status: updates program status label
def update_status(status_str):
    window_main.status_label.configure(text=status_str)
    print(status_str)

def adjustEdgeDectection():
    global edge_threshold
    edge_threshold = simpledialog.askinteger(
        "Input",
        "Current Value: " + str(edge_threshold) + "\nEnter edge threshold value (integer)",
        parent=window_main,
        minvalue=0,
        maxvalue=1000)
    update_status("Changed edge threshold to " + str(edge_threshold))

def adjustCircleDectection():
    global circle_threshold
    circle_threshold = simpledialog.askinteger(
        "Input",
        "Current Value: " + str(circle_threshold) + "\nEnter circle threshold value (integer)",
        parent=window_main,
        minvalue=0,
        maxvalue=1000)
    update_status("Changed circle threshold to " + str(circle_threshold))

def adjustSmallErrorAcceptance():
    global error_small
    error_small = simpledialog.askfloat(
        "Input",
        "Current Value: " + str(error_small) + "\nEnter circle threshold value (between 0 and 1)",
        parent=window_main,
        minvalue=0.01,
        maxvalue=0.99)
    update_status("Changed small error acceptance to " + str(error_small))

def adjustLargeErrorAcceptance():
    global error_large
    error_large = simpledialog.askfloat(
        "Input",
        "Current Value: " + str(error_large) + "\nEnter circle threshold value (between 0 and 1)",
        parent=window_main,
        minvalue=0.01,
        maxvalue=0.99)
    update_status("Changed large error acceptance to " + str(error_large))

def adjustResizePercentage():
    global resize_percentage
    resize_percentage = simpledialog.askfloat(
        "Input",
        "Current Value: " + str(resize_percentage) + "\nEnter resize percentage (between 0 and 1)",
        parent=window_main,
        minvalue=0.01,
        maxvalue=0.99)
    update_status("Changed resize percentage to " + str(resize_percentage))

def adjustBlur():
    global blur_kernel
    blur_kernel = simpledialog.askinteger(
        "Input",
        "Current Value: " + str(blur_kernel) + "\nEnter blur kernel size (odd integer)",
        parent=window_main,
        minvalue=3,
        maxvalue=2025)
    update_status("Changed blur kernel size to " + str(blur_kernel))

def resetValuesToDefualt():
    global edge_threshold, circle_threshold, error_small, error_large, resize_percentage, blur_kernel
    edge_threshold = d_edge_threshold
    circle_threshold = d_circle_threshold
    error_small = d_error_small * 0.01
    error_large = d_error_large * 0.01
    resize_percentage = d_resize_percentage * 0.01
    blur_kernel = d_blur_kernel

    # Set sliders to default
    window_main.slider_edge_threshold.set(d_edge_threshold)
    window_main.slider_circle_threshold.set(d_circle_threshold)
    window_main.slider_small_error.set(d_error_small)
    window_main.slider_large_error.set(d_error_large)
    window_main.slider_resize_percentage.set(d_resize_percentage)
    window_main.slider_blur_kernel.set(d_blur_kernel)

    update_status("All values reset to defaults.")

def toggleAdvancedSettings():
    global advanced_settings_shown

    if advanced_settings_shown:
        window_main.adjustment_frame.grid_forget()
        advanced_settings_shown = False
    else:
        window_main.adjustment_frame.grid(row=0, rowspan=6, column=6, sticky="NWES", pady=(12))
        advanced_settings_shown = True

# GUI CREATION #
# Create menu
menu = Menu(window_main)
file_items = Menu(menu, tearoff=0, bg=WHITE)
file_items.add_command(label="Load Image", command=load_image)
file_items.add_command(label="Save Output", command=save_image)
menu.add_cascade(label="File", menu=file_items)
adjust_items = Menu(menu, tearoff=0)
adjust_items.add_command(label="Edge Detection Sensitivity...", command=adjustEdgeDectection)
adjust_items.add_command(label="Circle Detection Sensitivity...", command=adjustCircleDectection)
adjust_items.add_command(label="Small Error Acceptance...", command=adjustSmallErrorAcceptance)
adjust_items.add_command(label="Large Error Acceptance...", command=adjustLargeErrorAcceptance)
adjust_items.add_command(label="Resize Percentage...", command=adjustResizePercentage)
adjust_items.add_command(label="Blur Kernel Size...", command=adjustBlur)
adjust_items.add_command(label="Reset Values to Default", command=resetValuesToDefualt)
menu.add_cascade(label="Adjust Values", menu=adjust_items)
menu.add_command(label="Show Advanced Settings", command=toggleAdvancedSettings)

window_main.config(menu=menu)

# Create preview box for image
window_main.image_canvas = tk.Canvas(window_main, width=600, height=570, relief="flat")
window_main.image_canvas.create_rectangle(0, 0, 600, 570, fill=BLACK)

# Create buttons
window_main.button_show_source = tk.Button(window_main, text="Show Source", font=(FONT_PRIMARY, 12), command=show_source, padx="10", bg=PRIMARY, fg=BLACK, relief="groove")
window_main.button_show_output = tk.Button(window_main, text="Show Output", font=(FONT_PRIMARY, 12), command=show_output, padx="10", bg=PRIMARY, fg=BLACK, relief="groove")
window_main.button_run = tk.Button(window_main, text="Run", font=(FONT_PRIMARY, 12), command=run, padx="10", bg=PRIMARY, fg=BLACK, relief="groove")

# Create output labels
window_main.lbl_title = tk.Label(window_main, text="Outputs", font=(FONT_PRIMARY, 12), bg=PRIMARY, fg=BLACK)
window_main.lbl_pennies_count = tk.Label(window_main, text="Pennies", font=(FONT_SECONDARY, 10), bg=PRIMARY, fg=BLACK)
window_main.lbl_nickles_count = tk.Label(window_main, text="Nickles", font=(FONT_SECONDARY, 10), bg=PRIMARY, fg=BLACK)
window_main.lbl_dimes_count = tk.Label(window_main, text="Dimes", font=(FONT_SECONDARY, 10), bg=PRIMARY, fg=BLACK)
window_main.lbl_quarters_count = tk.Label(window_main, text="Quarters", font=(FONT_SECONDARY, 10), bg=PRIMARY, fg=BLACK)
window_main.lbl_total_count = tk.Label(window_main, text="Total", font=(FONT_SECONDARY, 10), bg=PRIMARY, fg=BLACK)
window_main.lbl_pennies_count_num = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_pennies_count_cur = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_nickles_count_num = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_nickles_count_cur = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_dimes_count_num = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_dimes_count_cur = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_quarters_count_num = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_quarters_count_cur = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_total_count_num = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)
window_main.lbl_total_count_cur = tk.Label(window_main, text="0", font=(FONT_SECONDARY, 8), bg=PRIMARY, fg=BLACK)

# Create status label
status_str = "Choose a source image (under 'File/Load Image'), and press run."
window_main.status_label = tk.Label(window_main, text=status_str, font=("Arial", 8), bg=WHITE, fg=BLACK)

# Create adjustment panel
window_main.adjustment_frame = tk.Frame(window_main, bg=WHITE)
window_main.lbl_adjustment_panel_title = tk.Label(window_main.adjustment_frame, text="Adjustments", font=(FONT_PRIMARY, 12), bg=WHITE, fg=BLACK)
window_main.lbl_edge_threshold = tk.Label(window_main.adjustment_frame, text="Edge Threshold", font=(FONT_SECONDARY, 8), bg=WHITE, fg=BLACK)
window_main.slider_edge_threshold = tk.Scale(window_main.adjustment_frame, from_=1, to=500, bg=WHITE, orient=tk.HORIZONTAL)
window_main.slider_edge_threshold.set(d_edge_threshold)
window_main.lbl_circle_threshold = tk.Label(window_main.adjustment_frame, text="Circle Threshold", font=(FONT_SECONDARY, 8), bg=WHITE, fg=BLACK)
window_main.slider_circle_threshold = tk.Scale(window_main.adjustment_frame, from_=1, to=100, bg=WHITE, orient=tk.HORIZONTAL)
window_main.slider_circle_threshold.set(d_circle_threshold)
window_main.lbl_small_error = tk.Label(window_main.adjustment_frame, text="Small Error Percentage", font=(FONT_SECONDARY, 8), bg=WHITE, fg=BLACK)
window_main.slider_small_error = tk.Scale(window_main.adjustment_frame, from_=1, to=99, bg=WHITE, orient=tk.HORIZONTAL)
window_main.slider_small_error.set(d_error_small)
window_main.lbl_large_error = tk.Label(window_main.adjustment_frame, text="Large Error Percentage", font=(FONT_SECONDARY, 8), bg=WHITE, fg=BLACK)
window_main.slider_large_error = tk.Scale(window_main.adjustment_frame, from_=1, to=99, bg=WHITE, orient=tk.HORIZONTAL)
window_main.slider_large_error.set(d_error_large)
window_main.lbl_resize_percentage = tk.Label(window_main.adjustment_frame, text="Resize Percentage", font=(FONT_SECONDARY, 8), bg=WHITE, fg=BLACK)
window_main.slider_resize_percentage = tk.Scale(window_main.adjustment_frame, from_=1, to=99, bg=WHITE, orient=tk.HORIZONTAL)
window_main.slider_resize_percentage.set(d_resize_percentage)
window_main.lbl_blur_kernel = tk.Label(window_main.adjustment_frame, text="Blur Kernel", font=(FONT_SECONDARY, 8), bg=WHITE, fg=BLACK)
window_main.slider_blur_kernel = tk.Scale(window_main.adjustment_frame, from_=3, to=49, resolution=3, bg=WHITE, orient=tk.HORIZONTAL)
window_main.slider_blur_kernel.set(d_blur_kernel)
window_main.button_set_to_default = tk.Button(window_main.adjustment_frame, text="Set to Default", font=(FONT_PRIMARY, 12), command=resetValuesToDefualt, padx="10", bg=PRIMARY, fg=BLACK, relief="groove")


# GUI LAYOUT #
# Image preview
window_main.image_canvas.grid(row=0, column=0, rowspan=7, columnspan=6, sticky="NESW", padx=8, pady=8)

# Buttons
window_main.button_show_source.grid(row=8, column=0, sticky="NWE", padx=8, pady=2)
window_main.button_show_output.grid(row=9, column=0, sticky="NWE", padx=8, pady=2)
window_main.button_run.grid(row=10, column=0, rowspan=2, sticky="NWES", padx=8, pady=2)

# Output labels
window_main.lbl_title.grid(row=8, column=1, columnspan=5, sticky="NWES", padx=(0,8))
window_main.lbl_pennies_count.grid(row=9, column=1, sticky="NWES")
window_main.lbl_nickles_count.grid(row=9, column=2, sticky="NWES")
window_main.lbl_dimes_count.grid(row=9, column=3, sticky="NWES")
window_main.lbl_quarters_count.grid(row=9, column=4, sticky="NWES")
window_main.lbl_total_count.grid(row=9, column=5, sticky="NWES", padx=(0,8))
window_main.lbl_pennies_count_num.grid(row=10, column=1, sticky="NWES")
window_main.lbl_nickles_count_num.grid(row=10, column=2, sticky="NWES")
window_main.lbl_dimes_count_num.grid(row=10, column=3, sticky="NWES")
window_main.lbl_quarters_count_num.grid(row=10, column=4, sticky="NWES")
window_main.lbl_total_count_num.grid(row=10, column=5, sticky="NWES", padx=(0,8))
window_main.lbl_pennies_count_cur.grid(row=11, column=1, sticky="NWES")
window_main.lbl_nickles_count_cur.grid(row=11, column=2, sticky="NWES")
window_main.lbl_dimes_count_cur.grid(row=11, column=3, sticky="NWES")
window_main.lbl_quarters_count_cur.grid(row=11, column=4, sticky="NWES")
window_main.lbl_total_count_cur.grid(row=11, column=5, sticky="NWES", padx=(0,8))

# Status label
window_main.status_label.grid(row=12, column=0, columnspan=6, sticky="NWS", padx=8, pady=(12,0))

# Adjustment panel
window_main.adjustment_frame.grid(row=0, rowspan=6, column=6, sticky="NWES", pady=(12))
window_main.lbl_adjustment_panel_title.grid(row=0, column=6, sticky="NWES", pady=(0,20), padx=65)
window_main.lbl_edge_threshold.grid(row=1, column=6, sticky="NWS", padx=0)
window_main.slider_edge_threshold.grid(row=2, column=6, sticky="NWES", padx=0)
window_main.lbl_circle_threshold.grid(row=3, column=6, sticky="NWS", padx=0)
window_main.slider_circle_threshold.grid(row=4, column=6, sticky="NWES", padx=0)
window_main.lbl_small_error.grid(row=5, column=6, sticky="NWS", padx=0)
window_main.slider_small_error.grid(row=6, column=6, sticky="NWES", padx=0)
window_main.lbl_large_error.grid(row=7, column=6, sticky="NWS", padx=0)
window_main.slider_large_error.grid(row=8, column=6, sticky="NWES", padx=0)
window_main.lbl_resize_percentage.grid(row=9, column=6, sticky="NWS", padx=0)
window_main.slider_resize_percentage.grid(row=10, column=6, sticky="NWES", padx=0)
window_main.lbl_blur_kernel.grid(row=11, column=6, sticky="NWS", padx=0)
window_main.slider_blur_kernel.grid(row=12, column=6, sticky="NWES", padx=0)
window_main.button_set_to_default.grid(row=13, column=6, sticky="NWES", padx=6, pady=20)

# START #
toggleAdvancedSettings()
window_main.mainloop()