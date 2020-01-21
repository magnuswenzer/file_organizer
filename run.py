from gui.app import App 


if __name__ == '__main__': 
	root = App()
	root.state('zoomed')
	#w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	#root.geometry("%dx%d+0+0" % (w, h))
	root.mainloop()