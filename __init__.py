import cv2 as cv2
import numpy as np

import os

import datetime

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import matplotlib as mpl

"""Stolen from opencv readthedocs tutorial (full of mistakes, but well it helped) 
https://opencv-tutorial.readthedocs.io/en/latest/app/app.html
https://github.com/rasql/opencv-tutorial/blob/master/cvlib.py

but now its gonna be mpl app
"""

class Collection:
    """
    Class to attach stuff to (e.g., ax, gs, etc)
    """
    def __init__(self):
        pass

class EventHandler:
    def __init__(self,parent):
        self.parent = parent
        
        
    
    def button_redraw(self,event):
        self.parent.draw()
        
    def button_accept(self,event):
        self.parent.accept()
        
        
        
        
    def objstats_submit_classint(self,text):
        par = self.parent
        try:
            val = int(text)
        except:
            print("That box needs an int")
            if par.obj is not None:
                par.objstats.class_int.text.set_val(
                    par.objstats.class_int.text.fmt_func(par.obj.class_int)
                                                    )
            return
        
        if par.obj is not None:
            par.obj.class_int = val
            
    def objstats_submit_posx(self,text):
        par = self.parent
        try:
            val = float(text)
        except:
            print("That box needs an float")
            if par.obj is not None:
                par.objstats.posx.text.set_val(
                    par.objstats.posx.text.fmt_func(par.obj.pos[0])
                                                )
            return
        if par.obj is not None:
            pos = par.obj.pos
            pos[0] = val
            par.obj.pos = pos
    def objstats_submit_posy(self,text):
        par = self.parent
        try:
            val = float(text)
        except:
            print("That box needs an float")
            if par.obj is not None:
                par.objstats.posy.text.set_val(
                    par.objstats.posy.text.fmt_func(par.obj.pos[1])
                                                )
            return
        if par.obj is not None:
            pos = par.obj.pos
            pos[1] = val
            par.obj.pos = pos
            
    def objstats_submit_sizex(self,text):
        par = self.parent
        try:
            val = float(text)
        except:
            print("That box needs an float")
            if par.obj is not None:
                par.objstats.sizex.text.set_val(
                    par.objstats.sizex.text.fmt_func(par.obj.size[0])
                                                )
            return
        if par.obj is not None:
            size = par.obj.size
            size[0] = val
            par.obj.size = size
    def objstats_submit_sizey(self,text):
        par = self.parent
        try:
            val = float(text)
        except:
            print("That box needs an float")
            if par.obj is not None:
                par.objstats.sizey.text.set_val(
                    par.objstats.sizey.text.fmt_func(par.obj.size[1])
                                                )
            return
        if par.obj is not None:
            size = par.obj.size
            size[1] = val
            par.obj.size = size
            
    def findlightsettings_submit_threshold(self,text):
        
        par = self.parent
        try:
            val = int(text)
        except:
            print("That box needs an int")
            if par.obj is not None:
                par.findlightsettings.threshold.text.set_val(
                    par.findlightsettings.threshold.text.fmt_func(par.findlightsettings.threshold.val)
                                                )
            return
        
        par.findlightsettings.threshold.val = val
    def findlightsettings_submit_blurradius(self,text):
        
        par = self.parent
        try:
            val = int(text)
        except:
            print("That box needs an int")
            if par.obj is not None:
                par.findlightsettings.blurradius.text.set_val(
                    par.findlightsettings.blurradius.text.fmt_func(par.findlightsettings.blurradius.val)
                                                )
            return

        par.findlightsettings.blurradius.val = val

def fmt_pos(val):
    return "{:.3f}".format(val)
def fmt_size(val):
    return "{:.2f}".format(val)
def fmt_int(val):
    return "{}".format(val)
class mplApp:
    
    obj_options = dict(id=0,
                       color='g',
                       anchor=None,
                       )
    
    options = {
                'sel_color':'r',
                'obj_default_pos': [300,300],
                'obj_default_size': [40,40],
                
                'obj_speed': 1, 
                'obj_resize_speed': 1, 
                
                }
    
    def __init__(self,**kwargs):
        
        self.objs = []
        self.obj = None # Currently Selected
        
        self.obj_options = mplApp.obj_options.copy()
        
        # Setup
        self.events = EventHandler(self)
        self.key_locked = False # see self.key()
        
        self.go_to_next_image = False
        self.go_to_previous_image = False
        
        
        self.pressed_close = datetime.datetime.now()
        self.closing = False
        
        # Fix kwargs
        for k,val in kwargs.items():
            pass
        
        #  Keys        key : (function,help msg) # Functions have to accept "event"
        self.hotkeys = {
                        'f1': (self.key_help,"Help"),
                        'i': (self.inspect,"Inspect"),
                        'escape': (self.close,"Close"),
                        'n': (self.key_new_obj,"New object"),
                        'r': (self.key_redo_findlight,"Redo findlight (Set results to current object)"),
                        'c': (self.key_select_next_obj,"Cycle select object (alt: cycle faster). Hover object when press to select it"),
                        'C': (self.key_select_next_obj,"(shift+c) Cycle backwards select object (alt: cycle faster)"),
                        'x': (self.key_delete_obj,"Delete selected object"),
                        'v': (self.key_unselect_obj,"Unselect object"),
                        '[': (self.key_prev_img,"Previous Image"),
                        ']': (self.key_next_img,"Next Image"),
                        'enter': (self.key_accept_img,"Accept (write) results and next image"),
                        }
        
        
        # Lets go
        
        self.initialize_fig()
        
    def key_help(self,event):
        self.help()
    
    def help(self):
        
        print("--- Help ---")
        for k,v in self.hotkeys.items():
            print("  {}: {}".format(k,v[1]))
            
        print(" - Move selected object:")
        print("   Up-Left-Down-Right Arrows")
        print("   Shift: faster Shift+alt: Even faster")
        print("   Ctrl:  slower Ctrl+alt:  Even slower")
        print(" - Resize selected object:")
        print("   w-s: Vertical Bigger-Smaller. a-d Horizontal Smaller-Bigger")
        print("   q-e: Both Smaller-Bigger")
        print("   Shift: faster Shift+alt: Even faster")
        print("   Ctrl:  slower Ctrl+alt:  Even slower")
        print("--- OOOO ---")
            
    def inspect(self,event):
        print(" - Inspect")
        print("  ",self.objs,self.obj)
    
    def run(self):
        raise NotImplementedError("Needs implement in child")
            
    
    def initialize_fig(self,*args,**kwargs):
        
        from matplotlib.widgets import Slider,Button,TextBox,CheckButtons
        import matplotlib.gridspec as gridspec
        
        def make_input_box(gs,on_submit,fmt_func):
            thing = Collection()
            thing.ax = self.fig.add_subplot(gs)
            thing.text = LockingTextBox(thing.ax, "",textalignment='center')
            thing.text.on_submit(on_submit)
            thing.text.fmt_func = fmt_func
            thing.text.parent = self
            return thing
        def make_button(gs,on_click,text):
            thing = Collection()
            thing.ax = self.fig.add_subplot(gs)
            thing.button = Button(thing.ax, text)
            thing.button.on_clicked(on_click)
            return thing
        
        # Setup
        self.ax = Collection()
        
        
        # init vals
        
        gridspec_kwargs = { 'left': 0.05,
                            'right': 0.99,
                            'top': 0.99,
                            'bottom': 0.05,
                            'wspace': 0.15,
                            'hspace': 0.,
                            
                            'height_ratios': [4,1],
                            }
        
        ##### Prepare figure
        self.fig = plt.figure("Find Light",figsize=(7.5,4))
        self.gs = self.fig.add_gridspec(2,2,**gridspec_kwargs)
        
        ### Img axis
        self.ax.img = self.fig.add_subplot(self.gs[0, 0])
        
        # self.ax.img_bg = self.fig.add_subplot(self.gs[1, 0])
        
        self.ax.zoomed = self.fig.add_subplot(self.gs[0, 1])
        self.ax.zoomed.plot([0, 1], [0, 1], c=mplApp.options['sel_color'],transform=self.ax.zoomed.transAxes)
        self.ax.zoomed.plot([0, 1], [1, 0], c=mplApp.options['sel_color'],transform=self.ax.zoomed.transAxes)
        
        self.ax.img.im = None
        self.ax.img.im_bgsubtract = None
        
        self.ax.zoomed.im = None
        self.ax.zoomed.im_bgsubtract = None
        
        
        ### Buttons
        self.buttons = Collection()
        self.buttons.gs = self.gs[1,:].subgridspec(2,20,wspace=0.)#width_ratios=(1,3,3,3,3),
        
        # self.buttons.accept = make_button(self.buttons.gs[3,:],
        #                                     self.events.button_accept,
        #                                     "Accept",
        #                                   )
        # self.buttons.redraw = make_button(self.buttons.gs[4,:],
        #                                     self.events.button_redraw,
        #                                     "Redraw",
        #                                   )
        
        
        
        self.objstats = Collection()
        self.objstats.class_int = make_input_box(self.buttons.gs[1,0],
                                                    self.events.objstats_submit_classint,
                                                    fmt_int,
                                                    )
        self.objstats.posx      = make_input_box(self.buttons.gs[1,1:4],
                                                    self.events.objstats_submit_posx,
                                                    fmt_pos,
                                                    )
        self.objstats.posy      = make_input_box(self.buttons.gs[1,4:7],
                                                    self.events.objstats_submit_posy,
                                                    fmt_pos,
                                                    )
        self.objstats.sizex     = make_input_box(self.buttons.gs[1,7:10],
                                                    self.events.objstats_submit_sizex,
                                                    fmt_size,
                                                    )
        self.objstats.sizey     = make_input_box(self.buttons.gs[1,10:13],
                                                    self.events.objstats_submit_sizey,
                                                    fmt_size,
                                                    )
        # self.objstats.class_int.ax.text(0.,1.1,"Selected Object (class,x,y,w,h)", transform=self.objstats.class_int.ax.transAxes)
        self.objstats.class_int.ax.text(0.,1.5,"Selected Object", transform=self.objstats.class_int.ax.transAxes)
        self.objstats.class_int.ax.text(0.5,1.1,"Class", ha="center", transform=self.objstats.class_int.ax.transAxes)
        self.objstats.posx.ax.text(0.5,1.1,"x", ha="center", transform=self.objstats.posx.ax.transAxes)
        self.objstats.posy.ax.text(0.5,1.1,"y", ha="center", transform=self.objstats.posy.ax.transAxes)
        self.objstats.sizex.ax.text(0.5,1.1,"width", ha="center", transform=self.objstats.sizex.ax.transAxes)
        self.objstats.sizey.ax.text(0.5,1.1,"height", ha="center", transform=self.objstats.sizey.ax.transAxes)
        
        
        self.findlightsettings = Collection()
        self.findlightsettings.threshold = make_input_box(self.buttons.gs[1,15:17],
                                                    self.events.findlightsettings_submit_threshold,
                                                    fmt_int,
                                                    )
        self.findlightsettings.threshold.text.set_val(-1)
        
        self.findlightsettings.blurradius = make_input_box(self.buttons.gs[1,17:19],
                                                    self.events.findlightsettings_submit_blurradius,
                                                    fmt_int,
                                                    )
        self.findlightsettings.blurradius.text.set_val(-1)
        self.findlightsettings.threshold.ax.text(0.,1.5,"Find Light Settings", transform=self.findlightsettings.threshold.ax.transAxes)
        self.findlightsettings.threshold.ax.text(0.5,1.1,"Threshold", ha="center", transform=self.findlightsettings.threshold.ax.transAxes)
        self.findlightsettings.blurradius.ax.text(0.5,1.1,"BlurRadius", ha="center", transform=self.findlightsettings.blurradius.ax.transAxes)
        
        ### Key and mouse
        self.connect_canvas()
        self.remove_default_hotkeys()
        
        ### Show
        plt.show(block=False)
        
        
    def connect_canvas(self):
        self.mpl_connection_ids = []
        canvas = self.fig.canvas
        
        self.mpl_connection_ids.append( canvas.mpl_connect('key_press_event', self.key) )
        self.mpl_connection_ids.append( canvas.mpl_connect('button_press_event', self.mouse_click) )
        
        
    def remove_default_hotkeys(self):
        # remove some hotkeys from interactive
        plt.rcParams['keymap.home'].remove('r')
        plt.rcParams['keymap.home'].remove('h')
        plt.rcParams['keymap.save'].remove('s')
        plt.rcParams['keymap.save'].remove('ctrl+s')
        plt.rcParams['keymap.back'].remove('c')
        plt.rcParams['keymap.back'].remove('left')
        plt.rcParams['keymap.pan'].remove('p')
        plt.rcParams['keymap.zoom'].remove('o')
        plt.rcParams['keymap.fullscreen'].remove('f')
        plt.rcParams['keymap.forward'].remove('v')
        plt.rcParams['keymap.forward'].remove('right')
        plt.rcParams['keymap.quit'].remove('ctrl+w')
        plt.rcParams['keymap.quit'].remove('cmd+w')
        plt.rcParams['keymap.quit'].remove('q')
        # self.fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
        
        
    def disconnect_canvas(self):
        """Disconnect all callbacks."""
        
        for cid in self.mpl_connection_ids:
            self.fig.canvas.mpl_disconnect(cid)
    
    def mouse_click(self,event):
        
        # print("MOUSE CLIC",event.button)
        if event.button == 1: # left mouse
            if event.inaxes == self.ax.zoomed: # zoomed ax
                if self.obj is not None:
                    pos = [event.xdata,event.ydata]
                    self.move_selected(pos)

    def key(self, event):
        """Keypress handler"""
        if self.key_locked:
            return
        
        keys = event.key.split('+')
        event.modifiers = keys[:-1]
        event.k = keys[-1]
        k = event.k
        
        # print("key",event.modifiers,event.k)
        
        # if self.win is not None:
        #     ret = self.win.key(k)
        #     if ret:
        #         return True
        if k == 'up' or k == 'down' \
            or k == 'left' or k =='right':
            self.key_move_selected(event)
            return True
        
        if    k == 'w' or k == 'W' \
            or k == 'a' or k == 'A' \
             or k == 's' or k == 'S' \
              or k == 'd' or k == 'D' \
               or k == 'q' or k == 'Q' \
                or k == 'e' or k == 'E':
            self.key_resize_selected(event)
        
        if event.key in self.hotkeys:
            self.hotkeys[k][0](event)
            return True
        
        return False
    
    
    def key_accept_img(self,event):
        self.go_to_next_image = True
        self.accepted = True
    def key_next_img(self,event):
        self.go_to_next_image = True
    def key_prev_img(self,event):
        self.go_to_previous_image = True
    
    def close(self,event):
        if (datetime.datetime.now()-self.pressed_close).total_seconds() > 5:
            print("To close, press close again within 5s")
            self.pressed_close = datetime.datetime.now()
            return
        
        
        self.closing = True
        print("Close")
        plt.close(self.fig)
        
    
    def add_object( self, obj ):
        obj.set_parent(self)
        self.objs.append(obj)
    
    def key_new_obj(self,event):
        
        if self.fig is None:
            return
        
        if event.inaxes is not None:
            pos = [event.xdata,event.ydata]
        else:
            pos = self.options['obj_default_pos']
            
        ax = self.ax.img
        size = self.options['obj_default_size']
        
        obj = CrossedRectangle(pos,size=size,
                               color=self.obj_options['color'],
                               ax=ax)
        self.add_object(obj)
        self.select_obj(self.objs[-1])
        self.redraw_canvas()
        
    def key_move_selected(self,event):
        if self.obj is None:
            return
        
        modifiers = event.modifiers
        dir = event.k
        speed = mplApp.options['obj_speed']
        
        # Set speed
        if 'shift' in modifiers:
            speed *= 5
            if 'alt' in modifiers:
                speed *= 10
        elif 'ctrl' in modifiers or 'control' in modifiers:
            speed *= 0.5
            if 'alt' in modifiers:
                speed *= 0.5
        
        # Set New Position
        pos = self.obj.pos
        
        if dir == 'left':
            pos[0] += -speed
        elif dir == 'right':
            pos[0] += speed
        elif dir == 'up':
            pos[1] += -speed
        elif dir == 'down':
            pos[1] += speed
        
        self.move_selected(pos)
        
    def move_selected(self,pos):
        if self.obj is None:
            return
        self.obj.pos = pos
        
        self.update_zoomin()
        self.update_objstats()
        # self.redraw_canvas()
        
    def key_resize_selected(self,event):
        if self.obj is None:
            return
        
        modifiers = event.modifiers
        dir = event.k
        if dir.upper() == dir: # if uppercase..
            modifiers.append('shift')
        dir = dir.lower()
        speed = mplApp.options['obj_speed']
        
        # Set speed
        if 'shift' in modifiers:
            speed *= 5
            if 'alt' in modifiers:
                speed *= 10
        elif 'ctrl' in modifiers or 'control' in modifiers:
            speed *= 0.5
            if 'alt' in modifiers:
                speed *= 0.5
        
        # Set New Position
        w,h = self.obj.size
        if dir == 'w':
            h += speed
        elif dir == 's':
            h += -speed
        elif dir == 'a':
            w += -speed
        elif dir == 'd':
            w += speed
        elif dir == 'q':
            w += -speed
            h += -speed
        elif dir == 'e':
            w += speed
            h += speed
        # Limit size on lower end
        if w < 1:
            w = 1
        if h < 1:
            h = 1
        
        self.obj.size = w,h
        
        self.update_zoomin()
        self.update_objstats()
        # self.redraw_canvas()
        
    def key_unselect_obj(self,event):
        self.unselect_obj()
            
    def key_delete_obj(self,event):
        self.delete_obj()
        
        
    def key_select_next_obj(self,event):
        # if hovering an obj, select that one
        if event.inaxes == self.ax.img:
            for obj in self.objs:
                if obj.patch is not None:
                    contains, attrd = obj.patch.contains(event)
                    if contains:
                        self.select_obj(obj)
                        return
        # Else Select "next"
        shift = -1 if event.key.upper() == event.key else 1
        if 'alt' in event.modifiers:
            shift *= 10 #
        self.select_next_obj(shift=shift)
        
    def key_redo_findlight(self,event):
        self.do_findlight()
        self.update_zoomin()
        self.update_objstats()
        
    def select_obj(self,obj):
        if self.obj is not None:
            self.obj.selected = False # deselect
        
        obj.selected = True
        self.obj = obj
        
        self.update_zoomin()
        self.update_objstats()
        
    def select_next_obj(self, shift=1):
        """Select the next object, or the first in none is selected."""
        
        if len(self.objs) == 0:
            return
        
        if self.obj is None:
            i = -1
        else:
            i = self.objs.index(self.obj)
            self.objs[i].selected = False
        
        i = (i+shift) % len(self.objs)
        
        self.select_obj(self.objs[i])
    
    def unselect_obj(self):
        if self.obj is not None:
            self.obj.selected = False
            self.obj = None
            
            self.update_objstats()
            
    def delete_obj(self):
        if self.obj is not None:
            
            i = self.objs.index(self.obj)
            
            obj = self.objs.pop(i)
            obj.selected = False
            
            if obj.patch is not None:
                obj.patch.remove()
                
            
            del(obj)
            
            self.obj = None
            self.redraw_canvas()

    def delete_all_objs(self):
        
        while(len(self.objs)): # Get rid of em
            self.select_next_obj()
            self.delete_obj()
        return

    def update_zoomin(self):
        # Is called when a crosshair obj updates
        # Actually this should update using the self.selected
        if self.obj is None:
            # print("NO SELECTION")
            return
        if self.obj.patch is None:
            # print("NO PATCH")
            return
        obj = self.obj
        pos = obj.pos
        size = obj.size
        
        xmin,xmax = pos[0]-size[0]/2,pos[0]+size[0]/2
        ymin,ymax = pos[1]-size[1]/2,pos[1]+size[1]/2
        
        # See also set_clip_path
        self.ax.zoomed.set_xlim(xmin,xmax)
        self.ax.zoomed.set_ylim(ymax,ymin)
        
        self.redraw_canvas()
        
    
    def update_objstats(self):
        
        if self.obj is None: # Clear values
            self.objstats.class_int.text.set_val(-1)
            self.objstats.posx.text.set_val(-1)
            self.objstats.posy.text.set_val(-1)
            self.objstats.sizex.text.set_val(-1)
            self.objstats.sizey.text.set_val(-1)
        else:
            class_int = self.obj.class_int
            pos = self.obj.pos
            size = self.obj.size
            self.objstats.class_int.text.set_val(class_int)
            self.objstats.posx.text.set_val(self.objstats.posx.text.fmt_func(pos[0]))
            self.objstats.posy.text.set_val(self.objstats.posy.text.fmt_func(pos[1]))
            self.objstats.sizex.text.set_val(self.objstats.sizex.text.fmt_func(size[0]))
            self.objstats.sizey.text.set_val(self.objstats.sizex.text.fmt_func(size[1]))
            
        
    def redraw_canvas(self):
        if self.fig is not None:
            self.fig.canvas.draw()
    
    def reset_canvas_draw(self):
        # print("Draw")
        
        if self.ax.img.im is not None:
            self.ax.img.im.remove()
            del self.ax.img.im
            self.ax.img.im = None
        if self.ax.zoomed.im is not None:
            self.ax.zoomed.im.remove()
            del self.ax.zoomed.im
            self.ax.zoomed.im = None
        if self.ax.img.im_bgsubtract is not None:
            self.ax.img.im_bgsubtract.remove()
            del self.ax.img.im_bgsubtract
            self.ax.img.im_bgsubtract = None
        if self.ax.zoomed.im_bgsubtract is not None:
            self.ax.zoomed.im_bgsubtract.remove()
            del self.ax.zoomed.im_bgsubtract
            self.ax.zoomed.im_bgsubtract = None
        
        self.ax.img.clear()
        # self.ax.zoomed.clear() # Not the zoomed (Oh no the cross!)
        # self.ax.img_bg.clear()
        
        if self.img is not None:
            self.ax.img.im = self.ax.img.imshow(self.img)
            self.ax.zoomed.im = self.ax.zoomed.imshow(self.img)
        
        if self.img_bgsubtract is not None:
            self.ax.img.im.set_visible(not self.subtract_background_image)
            
            self.ax.img.im_bgsubtract = self.ax.img.imshow(self.img_bgsubtract)
            self.ax.img.im_bgsubtract.set_visible(self.subtract_background_image)
            
            self.ax.zoomed.im.set_visible(not self.subtract_background_image)
            
            self.ax.zoomed.im_bgsubtract = self.ax.zoomed.imshow(self.img_bgsubtract)
            self.ax.zoomed.im_bgsubtract.set_visible(self.subtract_background_image)
        
        self.ax.img.text(0,1.025,self.img_name_info,transform=self.ax.img.transAxes)
            
        self.redraw_canvas()
        

class Object:
    """Add an object to the current window."""
    lock = None # only one can be animated at a time
    def __init__(self, pos, **kwargs):
        
        pos = np.array(pos)
        
        self.patch = kwargs.pop('patch',None)
        self.parent = kwargs.pop('parent',None)
        
        # mplApp.objs.append(self)
        # App.win.obj = self # set self as current obj
        
        self.selected = False
        
        # kwargs # Watch out, this overwrites the defaults!! sounds very bad
        defaults = mplApp.obj_options
        defaults['id'] += 1
        self.id = defaults['id']
        
        self.color = kwargs.get('color',defaults['color'])
        
        anchor = kwargs.get('anchor',defaults['anchor'])
        self.set_anchor( anchor )
            
        self.set_pos(pos )
        self.class_int = kwargs.pop('class_int',0)
        
        self.hotkeys = {}
        
        # These are for moving 
        self.press = None
        self.background = None
        
        if self.patch is not None:
            self.connect()
        
        
    def __str__(self):
        return '<Object {} at ({}, {})>'.format(self.id, *self.pos)
    
    def set_parent(self,parent):
        self.parent = parent
    
    def set_pos(self, xy):
        if self.anchor is not None:
            xy = self.center_from_anchor(xy)
        if self.patch is not None:
            self.patch.set_x(xy[0]-self.patch.width/2)
            self.patch.set_y(xy[1]-self.patch.height/2)
        self._pos = list(xy)
    
    def get_pos(self):
        if self.patch is not None:
            x,y = self.patch.xy
            x = x + self.patch.width/2
            y = y + self.patch.height/2
            self._pos = [x,y]
        return self._pos

    def set_size(self, size):
        if self.patch is not None:
            # Adjust for anchor
            xy = self.patch.xy
            self.patch.set_x( xy[0] + (self.patch.width-size[0])/2. )
            self.patch.set_y( xy[1] + (self.patch.height-size[1])/2. )
            self.patch.width = size[0]
            self.patch.height = size[1]
        self._size = list(size)
    
    def get_size(self):
        if self.patch is not None:
            self._size = [self.patch.width,self.patch.height]
        return self._size
    
    
    def set_anchor(self, anchor: str) -> None:
        helpstr = """
        anchor: str of length 2
        concatenate:
        hor:  (l)eft (c)enter (r)ight
        vert: (t)op (m)iddle (b)ottom
        e.g., cm is center-middle
        exact position depends on shape (see e.g., rectangle)
        """
        err = False
        if anchor is None:
            err = False
        elif len(anchor) != 2:
            err = True
        elif anchor[0] not in 'lcr':
            err = True
        elif anchor[1] not in 'tmb':
            err = True
        
        if err:
            raise ValueError("Invalid Anchor: {}, {} ".format(anchor,helpstr))
        
        self.anchor = anchor
    def center_from_anchor(self, xy, options):
        # see e.g., rectangle
        return xy
    
    def draw(self):
        # see e.g., rectangle
        return False

    def is_inside(self, x, y):
        # see e.g., rectangle
        return False
    

    def connect(self):
        """Connect to all the events we need."""
        self.cidpress = self.patch.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.patch.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.patch.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        """Check whether mouse is over us; if so, store some data."""
        if (event.inaxes != self.patch.axes
                or Object.lock is not None):
            return
        contains, attrd = self.patch.contains(event)
        if not contains:
            return
        # print('event contains', self.patch.xy,self.pos)
        self.press = self.patch.xy, (event.xdata, event.ydata)
        Object.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.patch.figure.canvas
        axes = self.patch.axes
        self.patch.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.patch.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.patch)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        """Move the rectangle if the mouse is over us."""
        if (event.inaxes != self.patch.axes
                or Object.lock is not self):
            return
        (x0, y0), (xpress, ypress) = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.patch.set_x(x0+dx)
        self.patch.set_y(y0+dy)

        canvas = self.patch.figure.canvas
        axes = self.patch.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.patch)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        """Clear button press information."""
        if Object.lock is not self:
            return

        self.press = None
        Object.lock = None

        # turn off the rect animation property and reset the background
        self.patch.set_animated(False)
        self.background = None

        # Signal Parent that have changed
        if self.parent is not None:
            if self.selected:
                self.parent.update_zoomin()
                self.parent.update_objstats()
        
        # redraw the full figure
        self.patch.figure.canvas.draw()

    def disconnect(self):
        """Disconnect all callbacks."""
        self.patch.figure.canvas.mpl_disconnect(self.cidpress)
        self.patch.figure.canvas.mpl_disconnect(self.cidrelease)
        self.patch.figure.canvas.mpl_disconnect(self.cidmotion)
        
    def set_selected(self,selected):
        if self.patch is not None:
            if selected:
                color = mplApp.options['sel_color']
            else:
                color = self.color
            self.patch.set_edgecolor(color)
            
            self.patch.figure.canvas.draw()
        
        self._selected = selected
        
    def get_selected(self):
        return self._selected
        
    selected = property(get_selected,set_selected)
        
    pos = property(get_pos, set_pos)
    size = property(get_size, set_size)
    
    
class Rectangle(Object):
    def __init__(self, pos: np.ndarray,
                 size: list=[100,40],
                 border_thickness: int=1,
                 **kwargs):
        
        super().__init__(pos,**kwargs)
        
        self.size = w, h = size
        self.border_thickness = border_thickness
        
        self.ax = kwargs.pop('ax',None)
        
        fill = kwargs.pop('fill',False)
        
        
        if self.ax is not None:
            self.patch = self.get_default_patch(pos,w,h,color=self.color,fill=fill)
            self.ax.add_patch(self.patch)
            self.connect()
        
    def get_default_patch(self):
        return None
        # return mpatches.Rectangle(*args,**kwargs)
        
    def center_from_anchor(self, xy, options):
        w,h = self.size
        # Adjust for anchor
        if self.anchor[0] == 'l':
            xy[0] += w//2
        elif self.anchor[0] == 'r':
            xy[0] += -w//2
        if self.anchor[1] == 't':
            xy[1] += h//2
        elif self.anchor[1] == 'b':
            xy[1] += -h//2
        return xy
    
    def is_inside(self,x,y):
        x0, y0 = self.pos
        w, h = self.size
        return x0 <= x+w//2 <= x0+w and y0 <= y+h//2 <= y0+h
    

class CrossedRectangle(Rectangle):
    
    
    def get_default_patch(self,*args,**kwargs):
        
        patch = CrossedRectanglePatch(
            *args, **kwargs)
        return patch

class CrossedRectanglePatch(mpatches.PathPatch):
    """Note that rotating and other transforming doesnt work as is now
    
    """
    def __init__(self,*args,**kwargs):
        
        pos = args[0]
        size = [args[1],args[2]]
        
        xmin,xmax = pos[0]-size[0]/2,pos[0]+size[0]/2
        ymin,ymax = pos[1]-size[1]/2,pos[1]+size[1]/2
        
        self._x0 = xmin
        self._y0 = ymin
        self._width = size[0]
        self._height = size[1]
        
        self.make_path()
        
        super().__init__(self._path,**kwargs)
        
        
    def make_path(self):
        
        from matplotlib.path import Path
        
        xmin,xmax = self._x0,self._x0+self._width
        ymin,ymax = self._y0,self._y0+self._height
        
        pathdata = [
        (Path.MOVETO, (xmin,ymin)),
        (Path.LINETO, (xmax,ymax)),
        (Path.MOVETO, (xmax,ymin)),
        (Path.LINETO, (xmin,ymax)),
        (Path.MOVETO, (xmin,ymin)),
        
        (Path.LINETO, (xmax,ymin)),
        (Path.LINETO, (xmax,ymax)),
        (Path.LINETO, (xmin,ymax)),
        (Path.CLOSEPOLY, (xmin,ymin)),
        ]

        codes, verts = zip(*pathdata)
        self._path = Path(verts, codes)
        
        return self._path
        
    def get_path(self):
        if self.stale:
            self.make_path()
        return self._path
    
    def get_x(self):
        """Return the left coordinate of the rectangle."""
        return self._x0

    def get_y(self):
        """Return the bottom coordinate of the rectangle."""
        return self._y0

    def get_xy(self):
        """Return the left and bottom coords of the rectangle as a tuple."""
        return self._x0, self._y0

    def get_width(self):
        """Return the width of the rectangle."""
        return self._width

    def get_height(self):
        """Return the height of the rectangle."""
        return self._height

    def get_angle(self):
        """Get the rotation angle in degrees."""
        return self.angle

    def set_x(self, x):
        """Set the left coordinate of the rectangle."""
        self._x0 = x
        self.stale = True

    def set_y(self, y):
        """Set the bottom coordinate of the rectangle."""
        self._y0 = y
        self.stale = True

    def set_xy(self, xy):
        """
        Set the left and bottom coordinates of the rectangle.
        Parameters
        ----------
        xy : (float, float)
        """
        self._x0, self._y0 = xy
        self.stale = True

    def set_width(self, w):
        """Set the width of the rectangle."""
        self._width = w
        self.stale = True

    def set_height(self, h):
        """Set the height of the rectangle."""
        self._height = h
        self.stale = True
        
    def set_size(self,size):
        self._width = size[0]
        self._height = size[1]
        self.stale = True
    
    def get_size(self):
        return self._width,self._height

    def set_bounds(self, *args):
        """
        Set the bounds of the rectangle as *left*, *bottom*, *width*, *height*.
        The values may be passed as separate parameters or as a tuple::
            set_bounds(left, bottom, width, height)
            set_bounds((left, bottom, width, height))
        .. ACCEPTS: (left, bottom, width, height)
        """
        if len(args) == 1:
            l, b, w, h = args[0]
        else:
            l, b, w, h = args
        self._x0 = l
        self._y0 = b
        self._width = w
        self._height = h
        self.stale = True

    def get_bbox(self):
        """Return the `.Bbox`."""
        x0, y0, x1, y1 = self._convert_units()
        return mpl.transforms.Bbox.from_extents(x0, y0, x1, y1)

    xy = property(get_xy, set_xy)
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    size = property(get_size, set_size)
    

class LockingTextBox(mpl.widgets.TextBox):
    # From fariza at https://github.com/matplotlib/matplotlib/issues/7571/
    # which doesnt solve my keypress problem, so add another disconnect
    # Make sure to set self.parent
    # There has to be an extra self.started_typing because of the update_objstats calls, 
    # ALL (or at least many) textboxes are calling set_val() whenever someone types.
    started_typing = False
    def begin_typing(self, x=None): # x is deprecated
        if self.ignore({}):
            return
        super().begin_typing(x)
        # self.ax.figure.canvas.manager.toolmanager.keypresslock(self)
        self.parent.key_locked = True
        self.started_typing = True
        # print("begin_typing",self.text,self.parent.key_locked)

    def stop_typing(self):
        if self.ignore({}):
            return
        super().stop_typing()
        # self.ax.figure.canvas.manager.toolmanager.keypresslock.release(self)
        if self.started_typing:
            self.parent.key_locked = False
        self.started_typing = False
        # print("stop_typing",self.text,self.parent.key_locked)

def main():
    
    print("FindLightApp")
    print("DiD you mean the other?")
    # mplApp().run()
    
    import make_lll_detectlights_dataset
    make_lll_detectlights_dataset.main()
    
    
if __name__ == "__main__":
    main()