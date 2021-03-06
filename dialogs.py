#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dialogs.py
#
#  Copyright 2015 Tyler Dinsmoor <pappad@airmail.cc>
#


# Master Dialog modified for grid (tkSimpleDialog)
import Tkinter as tk
import ttk
import tkMessageBox
import os
import charGen
import random

class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        pass

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default='active')
        w.grid(row=0,column=0, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(row=0,column=1, padx=5, pady=5)

        #self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid(row=2)

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        return 1

    def apply(self):
        pass



class CharSheetGen(Dialog):

    def body(self, master):

        '''
        Just a text box for displaying generated sheet.
        Should use pages later to specify options for a custom sheet.
        '''

        self.title('Character Sheet Generator')
        self.char_gen_tabs = ttk.Notebook(self)
        self.char_gen_tabs.grid()

        self.show_page = tk.Frame(self)
        self.set_page = tk.Frame(self)

        self.char_gen_tabs.add(self.show_page, text='Sheet')
        self.char_gen_tabs.add(self.set_page, text='Settings')

        tk.Label(self.show_page, text="Generate a random character sheet.").grid(row=0, columnspan=2)
        self.char_text = tk.Text(self.show_page, width=50,
            height=30, state='disabled')
        self.char_text.grid(row=1, column=0)

        self.use_custom_b = tk.BooleanVar()
        use_custom = ttk.Checkbutton(self.set_page, variable=self.use_custom_b,
                    text='Custom Char').grid(row=0, column=0)

        self.pl_level = tk.Scale(self.set_page,
                orient='horizontal', from_=1, to=20, resolution=1,
                label='Level', length=200)
        self.pl_level.grid(row=1, column=0)
        self.pl_level.set(1)

        self.class_ch = tk.Listbox(self.set_page, selectmode='single')
        self.class_ch.grid(row=2, column=0)

        class_list = ('Cleric', 'Druid', 'Ranger', 'Paladin', 'Warlock', 'Wizard',
              'Barbarian', 'Fighter', 'Rouge', 'Monk', 'Bard', 'Sorcerer',
              'Commoner')
        for cl in class_list:
            self.class_ch.insert('end', cl)

        self.race_ch = tk.Listbox(self.set_page, selectmode='single')
        self.race_ch.grid(row=2, column=1)

        race_list = ('Human', 'Elf', 'Dwarf', 'Halfling', 'Half-Elf', 'Half-Orc',
            'Dragonborn', 'Gnome')
        for rc in race_list:
            self.race_ch.insert('end', rc)


        self.apply()

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="Next", width=10, command=self.ok, default='active')
        w.grid(row=0,column=0, padx=5, pady=5)
        w = tk.Button(box, text="Close", width=10, command=self.cancel)
        w.grid(row=0,column=1, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid(row=2)

    def ok(self, event=None):
        '''
        Need to replace stock ok() because I don't want it to exit
        immediately after creating a new sheet.
        '''
        self.mod_settings = self.parent.settings



        self.apply()

    def apply(self):

        #selected = self.class_ch.curselection()
        #class_name = str(self.class_ch.get(selected))
        #char_sheet = charGen.custom_param(self.parent.settings)

        char_sheet = charGen.custom_param(self.parent.settings)
        self.char_text.config(state='normal')
        self.char_text.delete(1.0, 'end')
        self.char_text.insert('end',char_sheet['Info'])
        self.char_text.config(state='disabled')



class SaveDialog(Dialog):

    def body(self, master):

        self.title('Save')
        l1 = tk.Label(master, text="Choose a name to save your area.")
        l1.grid(row=0, columnspan=2)
        l2 = tk.Label(master, text="Save Name:")
        l2.grid(row=1)
        self.e1 = tk.Entry(master)
        self.e1.grid(row=1, column=1)
        try:
            self.e1.insert(0, self.parent.cityName)
            return self.e1
        except:
            tkMessageBox.showerror('Error','No data to save!')
            self.cancel()

    def apply(self):

        save_name = str(self.e1.get())
        self.parent.save_all(save_name)

class SettingsMenu(Dialog):

    def body(self, master):
        self.title('Settings')

        self.settings_tabs = ttk.Notebook(self)
        self.settings_tabs.grid()

        self.party_page = tk.Frame(self)
        self.map_page = tk.Frame(self)
        self.town_page = tk.Frame(self)
        self.char_page = tk.Frame(self)

        self.settings_tabs.add(self.party_page,text="Party")
        self.settings_tabs.add(self.map_page,text="Map")
        self.settings_tabs.add(self.town_page,text="Towns")
        self.settings_tabs.add(self.char_page,text="Chars")

        def make_party_page():
            tk.Label(self.party_page, text="List your party members here").grid(row=0)
            self.partydesc = tk.Text(self.party_page, width=28, height=10)
            self.partydesc.grid(row=1)
            for char, lvl in self.parent.settings['party'].iteritems():
                self.partydesc.insert('end',"%s:%d\n"%(char, lvl))

        def make_map_page():
            biomes = ('Random','Marsh','Plains',
                    'Hills','Tundra',
                    'Desert','Forest')
            tk.Label(self.map_page, text="Biomes").grid(row=0)
            self.biome_listbox = tk.Listbox(self.map_page, selectmode='single')
            self.biome_listbox.grid(row=1)
            for biome in biomes:
                self.biome_listbox.insert('end', biome)
            self.biome_listbox.selection_set('0')

        def make_town_page():
            #tk.Label(self.town_page, text="Town Size").grid(row=0, column=0)
            self.city_size_mod_scale = tk.Scale(self.town_page,
                orient='horizontal', from_=0.1, to=3.0, resolution=0.1,
                label='Town Size', length=200)
            self.city_size_mod_scale.grid(row=0, column=1)
            self.city_size_mod_scale.set(1.0)

            self.affluence_scale = tk.Scale(self.town_page,
                orient='horizontal', from_=0.1, to=2.0, resolution=0.1,
                label='Affluence', length=200)
            self.affluence_scale.grid(row=1, column=1)
            self.affluence_scale.set(1.0)

        def make_char_page():
            tk.Label(self.char_page, text="Character Level").grid(row=0, column=0)
            self.level_scale = tk.Scale(self.char_page,
                orient='horizontal', from_=1, to=20)
            self.level_scale.grid(row=0, column=1)

        make_party_page()
        make_map_page()
        make_town_page()
        make_char_page()

    def apply(self):
        # Map Apply
        self.parent.settings['map']['biome'] = self.biome_listbox.get(
                                self.biome_listbox.curselection()).lower()
        if self.parent.settings['map']['biome'] == 'random':
            self.parent.settings['map']['biome'] = None
        # Town Apply
        self.parent.settings['town']['size_mod'] = self.city_size_mod_scale.get()
        self.parent.settings['town']['affluence'] = self.affluence_scale.get()
        # Char Apply
        self.parent.settings['char']['Level'] = self.level_scale.get()
        self.parent.parse_party(self.partydesc.get(1.0, 'end'))

class LoadDialog(Dialog):

    def body(self, master):

        self.title('Load')
        self.file_listbox = tk.Listbox(master, selectmode='single')
        self.get_save_dir()
        tk.Label(master,
            text="Choose a name to load your area.").grid(row=0,
                columnspan=2)
        self.file_listbox.grid(row=1, columnspan=2)
        self.del_opt = bool()
        self.del_cb = tk.Button(master, text="Delete",
            command=self.delete_save).grid(row=2, columnspan=2)

        self.bind("<Delete>", self.delete_save)

    def get_save_dir(self):

        self.file_listbox.delete(0, 'end')
        dir_list = os.listdir('save')
        for subfolder in dir_list:
            self.file_listbox.insert('end', subfolder)
        print "LoadDialog.get_save_dir.Done"

    def delete_save(self):

        selected = self.file_listbox.curselection()
        del_name = str(self.file_listbox.get(selected))
        try:
            os.remove('save/%s'%del_name)
            print "LoadDialog.delete_save.Done"
        except OSError:
            print "LoadDialog.delete_save.OSError['Item not a Dir?']"
        self.get_save_dir()


    def apply(self):
        try:
            selected = self.file_listbox.curselection()
            load_name = str(self.file_listbox.get(selected))
            self.parent.load_all(load_name)
        except Exception as err:
            print err
            tkMessageBox.showerror(
            "Error",err)

class EncounterDialog(Dialog):
    
    def body(self, master):
        self.master = master
        self.title('Encounter Generator')
        
        self.encounter_tabs = ttk.Notebook(self, height=300, width=650)
        self.encounter_tabs.grid(row=2, columnspan=4,sticky="w")

        self.details_page = tk.Frame(self, height=300, width=650)
        
        self.encounter_tabs.add(self.details_page,text="Settings")
        
        def make_details_page():
            
            types = ('humanoid','monstrosity','beast','undead','construct','fiend','plant')
            self.v = tk.StringVar()
            try:
                self.v.set(self.montypesave)
            except AttributeError:
                self.v.set(types[random.randint(0,len(types)-1)])
            
            for t in types:
                self.om = tk.OptionMenu(self, self.v, *types)
            tk.Label(self.details_page, text="Select Monster Type").grid(row=0)
            
            self.diff_choice = tk.StringVar()
            self.diff_om = tk.OptionMenu(self, self.diff_choice, "Random", "Easy", "Medium", "Hard", "Deadly")
            
            self.xplabel = tk.Label(self, fg="green")
            
            try:
                self.diff_choice.set(self.encdiffsave)
            except AttributeError:
                self.diff_choice.set("Random")
            self.om.grid(row=0, column=0)
            self.diff_om.grid(row=0, column=1)
            self.xplabel.grid(row=0, column=2)
            
        make_details_page()
        self.apply()

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default='active')
        w.grid(row=0,column=0, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(row=0,column=1, padx=5, pady=5)

        #self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid(row=0, column=3)

    def ok(self, event=None):
        '''
        Need to replace stock ok() because I don't want it to exit
        immediately after creating a new sheet.
        '''

        self.apply()

    def apply(self):
        import monGen
        montype = self.v.get()
        diffs = {
            'Random':random.randint(0,3),
            'Easy':0,
            'Medium':1,
            'Hard':2,
            'Deadly':3,
            }
        diff = diffs[self.diff_choice.get()]
        try:
            self.encounter_tabs.forget(self.details_page)
            enc = monGen.Encounter(self.parent, montype=montype, diff=diff)
            self.xplabel.config(text=str(enc.mons_xp))
            for mon in enc.mons:
                self.new_page = tk.Frame(self, height=300, width=650)
                self.encounter_tabs.add(self.new_page, text=mon['name'])
                m = tk.Message(self.new_page)
                txt = tk.Text(self.new_page, wrap='word', background=m.cget("background"), relief="flat",
                    borderwidth=0, font=m.cget("font"))
                txt.grid()
                m.destroy()
                txt.insert('end', mon['desc'])
                txt.insert('end', "\n")
        except Exception as e:
            print e
            self.montypesave = self.v.get()
            self.encdiffsave = self.diff_choice.get()
            self.encounter_tabs.destroy()
            self.om.destroy()
            self.diff_om.destroy()
            self.buttonbox()
            self.body(self.master)
            
        
