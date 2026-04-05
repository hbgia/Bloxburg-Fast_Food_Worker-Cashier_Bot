import utils
import quantity_and_size_classifier

main_dish = [
    6,      # ClassID of ORDER_Lettuce
    13,     # ClassID of ORDER_Tomato
    12,     #            ORDER_Patty
    14,     #            ORDER_VeganPatty
    2,      #            ORDER_Cheese
    9       #            ORDER_Onion
]

side_dish = [
    4,      # ORDER_Fries
    8,      # ORDER_MozzarellaStick
    10      # ORDER_OnionRing
]

drink = [
    3,      # ORDER_FountainDrink
    5,      # ORDER_FruityFruitJuice
    7       # ORDER_MilkShake
]

size_label_aliases = {
    '1': 'M',
    '2': 'S',
}
quantity_label_aliases = {
    'S': '2',
    'M': '1',
    'L': '1'
}

gui = [
    0,      # GUI_ServingMenu
    1,      # GUI_ServingState
    11,     # ORDER_OrderChatBox
]

idle_state = 0
main_state = 1
side_state = 2
drink_state = 3

def state_detects(detection_results: list) -> int:
    for object in detection_results:
        if object[0] in main_dish:
            return main_state
        
        if object[0] in side_dish:
            return side_state
        
        if object[0] in drink:
            return drink_state
        
    return idle_state

def determine_size(frame, detected_object: list):
    x0 = detected_object[1]
    y0 = detected_object[2]
    x2 = detected_object[3]
    y2 = detected_object[4]
    
    x1 = (x2 - x0) * 0.4 + x0
    y1 = (y2 - y0) * 0.4 + y0
    
    working_region = utils.crop_frame_copy(frame, x1, y1, x2, y2)
    # working_region = utils.crop_frame_copy(frame, x0, y0, x2, y2)
    
    return quantity_and_size_classifier.classify_frame(working_region)

def normalize_main_quantity(size_label: str) -> str:
    size_label = str(size_label).strip()
    if size_label in ('1', '2'):
        return size_label
    return quantity_label_aliases.get(size_label, '1')

def normalize_side_drink_size(size_label: str) -> str:
    size_label = str(size_label).strip()
    if size_label in ('S', 'M', 'L'):
        return size_label
    return size_label_aliases.get(size_label, 'M')


def process_order_on_state(frame, detection_results: list, state: int) -> list:
    if state == 0: return None
    
    order = []
    if state == 1:
        order.append([15, '1']) #if main state, add 1 bottom bun first. see servive_menu_offset.py for full id table
        for object in detection_results: # add the other
            if object[0] not in gui:
                size = determine_size(frame, object)
                order.append([object[0], normalize_main_quantity(size)])
        order.append([16, '1']) # if main state, add 1 top bun to finish
        
    elif state == 2 or state == 3:
        for object in detection_results:
            if object[0] not in gui:
                size = determine_size(frame, object)
                order.append(object[0])
                order.append(normalize_side_drink_size(size))
    return order


def get_GUI_menu_objects(detection_results:list) -> list:
    GUI_menu = [[],[]]
    
    for object in detection_results:
        if object[0] == 0:
            GUI_menu[0] = object
        elif object[0] == 1:
            GUI_menu[1] = object
        if (GUI_menu[0] and GUI_menu[1]): break
        
    return GUI_menu