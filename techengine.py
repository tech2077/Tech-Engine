#!/usr/bin/env python

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'
UP_KEY = 101
DOWN_KEY = 103
LEFT_KEY = 100
RIGHT_KEY = 102

# Number of the glut window.
window = 0

rotate_toggle = True
rtrix = 0
rtriy = 0
rcamx = 0
rcamy = 0
x_cord = 0
y_cord = 0
z_cord = -5.0

class vector:
	geotype = "vector"
	def __init__(self, *args):
		if len(args) == 3:
			self.coords = args
		elif len(args) == 2:
			self.coords = [args[0], args[1], 0]
		else:
			# x, y, z
			self.coords = [0, 0, 0]

class square:
	geotype = "square"
	def __init__(self, *args):
		if len(args) == 4:
			self.points = args
		else:
			# Top Left, Top Right, Bottom Right, Bottom Left
			self.points = [vector(-1, -1, 0), vector(1, -1, 0), vector(-1, 1, 0), vector(1, 1, 0)]

class square_scene:
	geotype = "scene"
	def __init__(self, filename, scenekey='scene'):
		self.scene = None
		envin = {}
		envin[scenekey] = self.scene
		scenefile = open(filename, "r").read()
		exec scenefile in envin
		self.scene = envin[scenekey]

class cube:
	geotype = "cube"
	bottom = 0
	top = 1
	front = 2
	back = 3
	left = 4
	right = 5
	def __init__(self, *args):
		self.s = [0, 0, 0, 0, 0, 0]

		if len(args) == 6:
			self.s = args
		else:
			'''
			Top
			Bottom
			Front
			Back
			Left
			Right
			'''
			self.s = [square(vector(-1, -1, -1), vector(1, -1, -1), vector(1, -1, 1), vector(-1, -1, 1)),
					 square(vector(1, 1, -1), vector(-1, 1, -1), vector(-1, 1, 1), vector(1, 1, 1)),
					 square(vector(1, 1, 1), vector(-1, 1, 1), vector(-1, -1, 1), vector(1, -1, 1)),
					 square(vector(-1, -1, -1), vector(1, -1, -1), vector(-1, 1, -1), vector(1, 1, -1)),
					 square(vector(1, 1, -1), vector(1, -1, -1), vector(1, -1, 1), vector(1, 1, 1)),
					 square(vector(-1, 1, 1), vector(-1, 1, -1), vector(-1, -1, -1), vector(-1, -1, 1))]


# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):			# We call this right after our OpenGL window is created.
    glEnable(GL_DEPTH_TEST)			# Enables Depth Testing
    glEnable(GL_COLOR_MATERIAL)
    # glEnable(GL_LIGHTING)			# Enable Lighting
    # glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)
    # glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)			# Enables Smooth Color Shading


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

# A timer function
def update(value):
	global rtriy
	global rotate_toggle
	if rotate_toggle:
		rtriy += 2.0
		if(rtriy > 360):
			rtriy -= 360
		glutPostRedisplay()
	glutTimerFunc(25, update, 0)

# The main drawing function. 
def DrawGLScene():
	global x_cord
	global y_cord
	global z_cord
	global rtrix
	global rtriy
	global rcamx
	global rcamy
	global scene

	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()					# Reset The View 

	glRotatef(rcamx, 1.0, 0.0, 0.0)
	glRotatef(rcamy, 0.0, 1.0, 0.0)
	glTranslatef(x_cord, y_cord, z_cord)

	'''
	ambientColor = (0.2, 0.2, 0.2, 1.0)
	lightColor0 = (0.5, 0.5, 0.5, 1.0)
	lightPos0 = (4.0, 0.0, 8.0, 1.0)
	lightColor1 = (0.5, 0.2, 0.2, 1.0)
	lightPos1 = (-1.0, 0.5, 0.5, 0.0)

	glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientColor)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
	glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
	glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
	glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
	'''

	glRotatef(rtrix, 1.0, 0.0, 0.0)
	glRotatef(rtriy, 0.0, 1.0, 0.0)
	glBegin(GL_QUADS)
	glColor3f(1.0, 1.0, 0.0)

	if scene.geotype == "scene":
		for i in scene.scene:
			for j in i:
				glVertex(j[0], j[1], j[2])
	if scene.geotype == "cube":
		for i in scene.s:
			for j in i.points:
				glVertex(j.coords[0], j.coords[1], j.coords[2])
	if scene.geotype == "square":
			for i in scene.points:
				glVertex(i.coords[0], i.coords[1], i.coords[2])

	glEnd()

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	global z_cord
	global x_cord
	global rotate_toggle
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		glutDestroyWindow(window)
		sys.exit()

	elif args[0] == 'r':
		rotate_toggle ^= True

	elif args[0] == 'a':
		x_cord += 0.2
	elif args[0] == 'd':
		x_cord -= 0.2
	elif args[0] == 'w':
		z_cord += 0.2
	elif args[0] == 's':
		z_cord -= 0.2

def speckeyPressed(*args):
	global rtrix
	global rtriy
	global rcamx
	global rcamy

	if args[0] == UP_KEY:
		rcamx += 2
		rtrix -= 3
	elif args[0] == DOWN_KEY:
		rcamx -= 2
		rtrix += 3
	elif args[0] == RIGHT_KEY:
		rcamy += 2
		rtriy -= 3
	elif args[0] == LEFT_KEY:
		rcamy -= 2
		rtriy += 3

def main():
	global window
	global scene

	if (len(sys.argv) > 1):
		if sys.argv[1] == "--square_test":
			scene = square()
		else:
			scene = square_scene(sys.argv[1])
	else:
		scene = cube()

	glutInit(())

	# Select type of Display mode:   
	#  Double buffer 
	#  RGB color
	#  Depth buffer
	glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# We have to make sure that we assign the window id to a global variable
	window = glutCreateWindow("Tech Engine")

   	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	
	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)
	glutSpecialFunc(speckeyPressed)

	# Register and initiate first call of timer function
	glutTimerFunc(25, update, 0)

	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine	
	glutMainLoop()

if __name__=="__main__":
	# Print message to console, and kick off the main to get it rolling.
	print "Hit ESC key to quit."
	main()