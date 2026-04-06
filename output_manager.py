import serving_menu_offset
import state_menu_offset
import time
import autoit
import input_manager

_DELAY = 0.25 # second(s)

def click_at(x, y, button='left', clicks=1, delay=0.1):
    # Validate coordinates
    if not isinstance(x, int) or not isinstance(y, int):
        raise ValueError("Coordinates must be integers.")
    if button not in ('left', 'right', 'middle'):
        raise ValueError("Button must be 'left', 'right', or 'middle'.")
    if clicks < 1:
        raise ValueError("Clicks must be >= 1.")

    # Move to position
    autoit.mouse_move(x, y)
    time.sleep(0.25)  # Small delay to ensure movement

    # Perform clicks
    for _ in range(clicks):
        autoit.mouse_click(button, x, y, 1)
        time.sleep(delay)
        
def determine_click_coor(x1, y1, x2, y2, offset_x2, offset_y2):
    x = (x2 - x1) * offset_x2 + x1
    y = (y2 - y1) * offset_y2 + y1
    return x, y
        
def click_state(state_menu: list, state: int):
    offset_x = state_menu_offset.state_menu_GUI_offset[state][0]
    offset_y = state_menu_offset.state_menu_GUI_offset[state][1]
    x1 = state_menu[1]
    y1 = state_menu[2]
    x2 = state_menu[3]
    y2 = state_menu[4]
    x, y = determine_click_coor(x1, y1, x2, y2, offset_x, offset_y)
    click_at(int(x), int(y))
    
def click_order_main(serving_menu: list, main_order: list):
    for object in main_order:
        offset_x = serving_menu_offset.main_dish_GUI_offset[object[0]][0]
        offset_y = serving_menu_offset.main_dish_GUI_offset[object[0]][1]
        x1 = serving_menu[1]
        y1 = serving_menu[2]
        x2 = serving_menu[3]
        y2 = serving_menu[4]
        x, y = determine_click_coor(x1, y1, x2, y2, offset_x, offset_y)
        click_at(int(x), int(y), clicks=int(object[1]), delay=_DELAY)
        
def click_order_side_drink(serving_menu: list, side_order: list):
    offset_x = serving_menu_offset.side_dish_GUI_offset[side_order[0]][0]
    offset_y = serving_menu_offset.side_dish_GUI_offset[side_order[0]][1]
    size_offset_x = serving_menu_offset.side_dish_GUI_offset[side_order[1]][0]
    size_offset_y = serving_menu_offset.side_dish_GUI_offset[side_order[1]][1]
    
    click_x1 = serving_menu[1]
    click_y1 = serving_menu[2]
    click_x2 = serving_menu[3]
    click_y2 = serving_menu[4]
    size_click_x1 = serving_menu[1]
    size_click_y1 = serving_menu[2]
    size_click_x2 = serving_menu[3]
    size_click_y2 = serving_menu[4]
    
    click_x, click_y = determine_click_coor(click_x1, click_y1, click_x2, click_y2, offset_x, offset_y)
    size_click_x, size_click_y = determine_click_coor(size_click_x1, size_click_y1, size_click_x2, size_click_y2, size_offset_x, size_offset_y)
    
    click_at(int(click_x), int(click_y))
    time.sleep(_DELAY)
    click_at(int(size_click_x), int(size_click_y))
    

def execute_order(GUI_menu: list, main_order: list, side_order: list, drink_order: list):
    serving_menu = GUI_menu[0]
    state_menu = GUI_menu[1]
    
    # execute main
    click_state(state_menu, 1)
    time.sleep(_DELAY)
    click_order_main(serving_menu, main_order)
    time.sleep(_DELAY)
    
    # execute side
    click_state(state_menu, 2)
    time.sleep(_DELAY)
    click_order_side_drink(serving_menu, side_order)
    time.sleep(_DELAY)
    
    # execute drink
    if drink_order:
        click_state(state_menu, 3)
        time.sleep(_DELAY)
        click_order_side_drink(serving_menu, drink_order)
        time.sleep(_DELAY)
    
    # finish up
    click_state(state_menu, 0)
    time.sleep(1)
    
def repeat_order(offset_x=0.5, offset_y=0.97):
    left, top, width, height = input_manager.get_primary_monitor_bounds()
    click_x = int(left + width * offset_x)
    click_y = int(top + height * offset_y)
    click_at(click_x, click_y)
    print(f"Repeat order click at: ({click_x}, {click_y})")