import object_detector
import input_manager
import output_manager
import logic
import time

_TIMEOUT = 10
_WAIT_EACH_ORDER = 2

main_order  = []
side_order  = []
drink_order = []
state = -1 # init int state

GUI_menu = []

timeout = _TIMEOUT
wait_each_order = _WAIT_EACH_ORDER

while True:
    frame = input_manager.take_full_screenshot()
    detection_results = object_detector.detect_objects(frame)
    # print(f"Deteded:\n{detection_results}")
    
    GUI_menu = logic.get_GUI_menu_objects(detection_results)
    
    state = logic.state_detects(detection_results)
    print(f"State detected: {state}")

    repeat_condition = (
        len(detection_results) <= 3 
        and state == 0
    )
    if repeat_condition:
        if timeout > 0:
            timeout = timeout - 1
        else:
            print("Timeout!")
            print("Repeating...")
            output_manager.press_key("e")
            output_manager.repeat_order()
            timeout = _TIMEOUT
    else:
        timeout = _TIMEOUT
    
    if (
        state == 1 
        and not main_order
    ): # if main state and main_order is empty
        main_order = logic.process_order_on_state(frame, detection_results, state)
        print(f"Main order collected: {main_order}")
        wait_each_order = _WAIT_EACH_ORDER
        
    elif (
        state == 2 
        and not side_order
    ): # same as above
        side_order = logic.process_order_on_state(frame, detection_results, state)
        print(f"Side order collected: {side_order}")
        wait_each_order = _WAIT_EACH_ORDER
        
    elif (
        state == 3 
        and not drink_order
    ):
        drink_order = logic.process_order_on_state(frame, detection_results, state)
        print(f"Drink order collected: {drink_order}")
        wait_each_order = _WAIT_EACH_ORDER
    
    elif (
        state == 0
        and GUI_menu
        and main_order
        and side_order
    ):
        if (wait_each_order > 0):
            wait_each_order = wait_each_order - 1
        else:
            print("Executing...")
            output_manager.execute_order(GUI_menu, main_order, side_order, drink_order)
            main_order.clear()
            side_order.clear()
            drink_order.clear()
            print("Completed! Clearing orders.")
            wait_each_order = _WAIT_EACH_ORDER

    time.sleep(1)