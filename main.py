from ui import *

if __name__ == '__main__':
    root = Window(min_size=(650, 435), fg_color='black')
    root.resizable(False, False)
    root.attributes('-alpha', 0.0)
    root.after(0, lambda: root.attributes('-alpha', 1.0))  # TODO change time to *more*, test on weaker laptop

    main_window = MainWindow(master=root, info_window=None, display_window=None, setup_window=None)

    info_window = InfoWindow()
    setup_window = SetupWindow(master=root, main_window=main_window)
    display_window = DisplayWindow(master=root, src_file=None, verified_key=None, main_window=main_window)

    # This seems completely illogical (and most probably is), but this is the only solution I could have found to
    # basically create the equivalence of a circular import. This stupidity works only because the MainWindow.__init__
    # saves these objects as a variable, but doesn't use them until some user input. Basically, it works unless the
    # user finds a way to interact with widgets before main_window.update_objects() is called,
    # which *should* be impossible
    main_window.update_objects(new_info_window_obj=info_window, new_setup_obj=setup_window,
                               new_display_window_obj=display_window)

    root.mainloop()
