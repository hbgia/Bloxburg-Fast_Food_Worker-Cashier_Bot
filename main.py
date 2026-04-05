import object_detector
import input_manager
import output_manager
import logic
import time

main_order  = []
side_order  = []
drink_order = []
state = -1 # init int state

GUI_menu = []

while True:
    frame = input_manager.take_full_screenshot()
    detection_results = object_detector.detect_objects(frame)
    # print(f"Deteded:\n{detection_results}")
    
    GUI_menu = logic.get_GUI_menu_objects(detection_results)
    
    state = logic.state_detects(detection_results)
    print(f"State detected: {state}")
    
    if (
        state == 1 
        and not main_order
    ): # if main state and main_order is empty
        main_order = logic.process_order_on_state(frame, detection_results, state)
        print(f"Main order collected: {main_order}")
        
    elif (
        state == 2 
        and not side_order
    ): # same as above
        side_order = logic.process_order_on_state(frame, detection_results, state)
        print(f"Side order collected: {side_order}")
        
    elif (
        state == 3 
        and not drink_order
    ):
        drink_order = logic.process_order_on_state(frame, detection_results, state)
        print(f"Drink order collected: {drink_order}")
        
    elif (
        state == 0
        and GUI_menu
        and main_order
        and side_order
    ):
        print("Executing...")
        output_manager.execute_order(GUI_menu, main_order, side_order, drink_order)
        main_order.clear()
        side_order.clear()
        drink_order.clear()
        print("Completed! Clearing orders.")
    
    time.sleep(1)