import pygame,os,sys,Tkinter,time,random
from pygame.locals import *
from threading import Thread
from settings import *
sys.path.append(os.getcwd() + "\\classes\\interfaces") # All the interface classes
sys.path.append(os.getcwd() + "\\classes\\utility")    # All the utility classes and the cross class functions



from functions import *
from datamanagement import * 
import reaction_classes
import category_classes 
import events_classes
import species_classes 
import kvalues_classes
import experimentalData_classes
import fittingData_classes
import reactionRates_classes
import deterministic_simulation_classes
import stochastic_simulation_classes
import results_classes
import database_management_classes
import sensitivity_analysis_classes
import michaelis_menten_classes
import ctypes
#import matplotlib
#import matplotlib.backends.backend_tkagg

# If the screen flashes away when running fullscreen comment out line 98 in matplotlib.backends.backend_tkagg, create a blank line below it and write pass (indentation similar to commented-out line)
# launch settings.py to fix this

db_tables = ('reactions','species','categories','k_values','settings','experimental_data','events')
db = database(db_tables)

                    
class storeDB(Thread):
    def __init__(self,table):
        self.table = table
        Thread.__init__(self)
        
    def run(self):
        global db
        db.storeFull(self.table)
        db.update(self.table)


class imageLoader(Thread):
    
    def __init__(self):
        self.system_images = {}
        self.system_images_loaded = False
        Thread.__init__(self) 
        
    def run(self):
    #global controls
        self.system_images['scrollbar_control'] = pygame.image.load('system_resources\\scrollbar_control.png').convert_alpha()
        self.system_images['horizontal_scrollbar_control'] = pygame.image.load('system_resources\\horizontal_scrollbar_control.png').convert_alpha()
        self.system_images['load_unit1'] = pygame.image.load('system_resources\\load_unit1.png').convert_alpha()
        self.system_images['load_unit2'] = pygame.image.load('system_resources\\load_unit2.png').convert_alpha()
        self.system_images['load_start'] = pygame.image.load('system_resources\\load_start.png').convert_alpha()
        self.system_images['load_end'] = pygame.image.load('system_resources\\load_end.png').convert_alpha()
    
    #categories
        self.system_images['categories_add'] = pygame.image.load('system_resources\\categories_add_category.png').convert_alpha()
        self.system_images['categories_edit'] = pygame.image.load('system_resources\\categories_edit_category.png').convert_alpha()
        
    #backgrounds
#         self.system_images['menu_interface_v2'] = pygame.image.load('system_resources\\menu_interface2.png').convert()
        self.system_images['menu_interface_v3'] = pygame.image.load('system_resources\\menu_interface3.png').convert()
        self.system_images['categories_background'] = pygame.image.load('system_resources\\categories_background.png').convert()
        self.system_images['events_background'] = pygame.image.load('system_resources\\events_background.png').convert()
        self.system_images['reactions_background'] = pygame.image.load('system_resources\\reactions_background.png').convert()
        self.system_images['reactions_background_top'] = pygame.image.load('system_resources\\reactions_background_top.png').convert()
        self.system_images['species_background'] = pygame.image.load('system_resources\\species_background.png').convert()
        self.system_images['deterministic_background'] = pygame.image.load('system_resources\\deterministic_background.png').convert()
        self.system_images['stochastic_background'] = pygame.image.load('system_resources\\stochastic_background.png').convert()
        self.system_images['loadData_background'] = pygame.image.load('system_resources\\loadData_background.png').convert()
        self.system_images['fittingData_background'] = pygame.image.load('system_resources\\fittingData_background.png').convert()
        self.system_images['reactionRates_background'] = pygame.image.load('system_resources\\reactionRates_background.png').convert()
        self.system_images['results_background'] = pygame.image.load('system_resources\\results_background.png').convert()
        self.system_images['database_management_background'] = pygame.image.load('system_resources\\database_management_background.png').convert()
        self.system_images['sensitivity_analysis_background'] = pygame.image.load('system_resources\\sensitivity_analysis_background.png').convert()
        self.system_images['michaelis_menten_background'] = pygame.image.load('system_resources\\michaelis_menten_background.png').convert()
        
        
    #deterministic simulation
        self.system_images['deterministic_background_results'] = pygame.image.load('system_resources\\deterministic_background_results.png').convert()
        self.system_images['deterministic_background_results'] = pygame.image.load('system_resources\\deterministic_background_results.png').convert()
        self.system_images['deterministic_background_results'] = pygame.image.load('system_resources\\deterministic_background_results.png').convert()
        self.system_images['deterministic_background_results_wide'] = pygame.image.load('system_resources\\deterministic_background_results_wide.png').convert()
        self.system_images['deterministic_background_results_top_wide'] = pygame.image.load('system_resources\\deterministic_background_results_top_wide.png').convert_alpha()
        self.system_images['chart_icon'] = pygame.image.load('system_resources\\chart_icon.png').convert_alpha()
        self.system_images['chart_icon_offline'] = pygame.image.load('system_resources\\chart_icon_offline.png').convert_alpha()
        self.system_images['running_simulation'] =  pygame.image.load('system_resources\\running_simulation.png').convert_alpha()
        self.system_images['run_simulation_button'] =  pygame.image.load('system_resources\\run_simulation_button.png').convert_alpha()
        self.system_images['run_simulation_button_disabled'] =  pygame.image.load('system_resources\\run_simulation_button_disabled.png').convert_alpha()
        self.system_images['abort'] = pygame.image.load('system_resources\\abort.png').convert_alpha()
        self.system_images['history_folder'] = pygame.image.load('system_resources\\history_folder.png').convert_alpha()
        self.system_images['CPU_toggled'] = pygame.image.load('system_resources\\CPU_toggled.png').convert_alpha()
        self.system_images['GPU_toggled'] = pygame.image.load('system_resources\\GPU_toggled.png').convert_alpha()
    
    #reactions
        self.system_images['one_sided_reaction'] = pygame.image.load('system_resources\\reaction_fields_single.png').convert_alpha()
        self.system_images['two_sided_reaction'] = pygame.image.load('system_resources\\reaction_fields_double.png').convert_alpha()
        self.system_images['reaction_linked'] = pygame.image.load('system_resources\\reaction_linked.png').convert_alpha()
        self.system_images['reaction_unlinked'] = pygame.image.load('system_resources\\reaction_unlinked.png').convert_alpha()
        self.system_images['reactions_k1_constrained'] = pygame.image.load('system_resources\\reactions_k1_constrained.png').convert_alpha()
        self.system_images['reactions_k_1_constrained'] = pygame.image.load('system_resources\\reactions_k_1_constrained.png').convert_alpha()
        self.system_images['reactions_topBar'] = pygame.image.load('system_resources\\reactions_topBar.png').convert_alpha()
        self.system_images['link_indicator'] = pygame.image.load('system_resources\\link_indicator.png').convert_alpha()
        self.system_images['save_button'] = pygame.image.load('system_resources\\save_button.png').convert_alpha()
        self.system_images['entree'] = pygame.image.load('system_resources\\entree_symbol.png').convert_alpha()
        self.system_images['entree_open'] = pygame.image.load('system_resources\\open_entree_symbol.png').convert_alpha()
        self.system_images['arrow'] = pygame.image.load('system_resources\\arrow.png').convert_alpha()
        self.system_images['arrow_eq'] = pygame.image.load('system_resources\\arrow_eq.png').convert_alpha()
        self.system_images['1_over_v'] = pygame.image.load('system_resources\\1_over_v.png').convert_alpha()
        self.system_images['1_over_v_small'] = pygame.image.load('system_resources\\1_over_v_small.png').convert_alpha()
        self.system_images['1_over_v_offline'] = pygame.image.load('system_resources\\1_over_v_offline.png').convert_alpha()
        self.system_images['preview_simulation'] = pygame.image.load('system_resources\\preview_simulation.png').convert_alpha()
        self.system_images['preview_simulation_offline'] = pygame.image.load('system_resources\\preview_simulation_offline.png').convert_alpha()
        self.system_images['preview_simulation_stochastic'] = pygame.image.load('system_resources\\preview_simulation_stochastic.png').convert_alpha()
        self.system_images['preview_simulation_stochastic_offline'] = pygame.image.load('system_resources\\preview_simulation_stochastic_offline.png').convert_alpha()
            
    #species
        self.system_images['species_editfield'] = pygame.image.load('system_resources\\species_amount_editing_field.png').convert_alpha()
        self.system_images['artificial_species_popup'] = pygame.image.load('system_resources\\artificial_species_popup.png').convert_alpha()
        self.system_images['operation_type_0'] = pygame.image.load('system_resources\\operation_type_0.png').convert_alpha()
        self.system_images['operation_type_1'] = pygame.image.load('system_resources\\operation_type_1.png').convert_alpha()
        self.system_images['operation_type_2'] = pygame.image.load('system_resources\\operation_type_2.png').convert_alpha()
        self.system_images['operation_type_3'] = pygame.image.load('system_resources\\operation_type_3.png').convert_alpha()
        
    #experimentalDatasets
        self.system_images['time_or_species'] = pygame.image.load('system_resources\\time_or_species.png').convert_alpha()
        self.system_images['time'] = pygame.image.load('system_resources\\time.png').convert_alpha()
        self.system_images['species'] = pygame.image.load('system_resources\\species.png').convert_alpha()
        self.system_images['line'] = pygame.image.load('system_resources\\line.png').convert_alpha()
        self.system_images['add_initial_conditions'] = pygame.image.load('system_resources\\add_initial_conditions.png').convert_alpha()
        self.system_images['update_initial_conditions'] = pygame.image.load('system_resources\\update_initial_conditions.png').convert_alpha()
        self.system_images['update_all_initial_conditions'] = pygame.image.load('system_resources\\update_all_initial_conditions.png').convert_alpha()
        self.system_images['edit_initial_conditions'] = pygame.image.load('system_resources\\edit_initial_conditions.png').convert_alpha()
        self.system_images['edit_events'] = pygame.image.load('system_resources\\edit_events.png').convert_alpha()
        self.system_images['view_as_graphs'] = pygame.image.load('system_resources\\view_as_graphs.png').convert_alpha()
        self.system_images['view_as_data'] = pygame.image.load('system_resources\\view_as_data.png').convert_alpha()
        self.system_images['apply_time_to_all'] = pygame.image.load('system_resources\\apply_time_to_all.png').convert_alpha()
        self.system_images['time_control_applied'] = pygame.image.load('system_resources\\time_control_applied.png').convert_alpha()
        
    #fitting
        self.system_images['start_fitting'] = pygame.image.load('system_resources\\start_fitting_uniform.png').convert_alpha()
        self.system_images['initiate_refit'] = pygame.image.load('system_resources\\initiate_refit.png').convert_alpha()
        self.system_images['fitting_data'] = pygame.image.load('system_resources\\fitting_data.png').convert_alpha()
        self.system_images['stop_fitting'] = pygame.image.load('system_resources\\stop_fitting_uniform.png').convert_alpha()
        self.system_images['stop_fitting_offline'] = pygame.image.load('system_resources\\stop_fitting_uniform_offline.png').convert_alpha()
        self.system_images['finished_fit'] = pygame.image.load('system_resources\\finished_fit.png').convert_alpha()
        self.system_images['apply_fit'] = pygame.image.load('system_resources\\apply_fit_uniform.png').convert_alpha()
        self.system_images['applied_fit'] = pygame.image.load('system_resources\\applied_fit.png').convert_alpha()
        self.system_images['applied_fit_blue'] = pygame.image.load('system_resources\\applied_fit_blue.png').convert_alpha()
        self.system_images['apply_fit_offline'] = pygame.image.load('system_resources\\apply_fit_uniform_offline.png').convert_alpha()
        self.system_images['higher_fitness'] = pygame.image.load('system_resources\\higher_fitness.png').convert_alpha()
        self.system_images['higher_fitness_offline'] = pygame.image.load('system_resources\\higher_fitness_offline.png').convert_alpha()
        self.system_images['refine_fitness'] = pygame.image.load('system_resources\\refine_fitness.png').convert_alpha()
        self.system_images['abort_fit'] = pygame.image.load('system_resources\\abort_fit.png').convert_alpha()
        self.system_images['examine_dataset'] = pygame.image.load('system_resources\\examine_dataset.png').convert_alpha()
        self.system_images['fitting_method_genetic'] = pygame.image.load('system_resources\\fitting_method_genetic.png').convert_alpha()
        self.system_images['fitting_method_mathematic'] = pygame.image.load('system_resources\\fitting_method_mathematic.png').convert_alpha()
        
    #reaction rates
        self.system_images['reactionRates_top'] = pygame.image.load('system_resources\\reactionRates_top.png').convert_alpha()
        self.system_images['indicator'] = pygame.image.load('system_resources\\indicator.png').convert_alpha()
        self.system_images['indicator_small'] = pygame.image.load('system_resources\\indicator_small.png').convert_alpha()
        self.system_images['restore_button'] = pygame.image.load('system_resources\\restore_button.png').convert_alpha()
        self.system_images['restore_all_button'] = pygame.image.load('system_resources\\restore_all_button.png').convert_alpha()
        
    #events
        self.system_images['add_events'] = pygame.image.load('system_resources\\add_events.png').convert_alpha()
        
    #database management
        self.system_images['add_database'] = pygame.image.load('system_resources\\add_database.png').convert_alpha()
        self.system_images['delete_popup'] = pygame.image.load('system_resources\\delete_popup.png').convert_alpha()
        self.system_images['name_popup'] = pygame.image.load('system_resources\\name_popup.png').convert_alpha()
        
    #results
        self.system_images['select_dataset'] = pygame.image.load('system_resources\\select_dataset.png').convert_alpha()
        self.system_images['add_species_to_plot'] = pygame.image.load('system_resources\\add_species_to_plot.png').convert_alpha()
        self.system_images['add_species_to_plot_offline'] = pygame.image.load('system_resources\\add_species_to_plot_offline.png').convert_alpha()
        self.system_images['view_as_concentration'] = pygame.image.load('system_resources\\view_as_concentration.png').convert_alpha()
        self.system_images['view_as_molecules'] = pygame.image.load('system_resources\\view_as_molecules.png').convert_alpha()  
        self.system_images['scatterplot_select'] = pygame.image.load('system_resources\\scatterplot_select.png').convert_alpha()
        self.system_images['scatterplot_selected'] = pygame.image.load('system_resources\\scatterplot_selected.png').convert_alpha()
        self.system_images['hard_drive'] = pygame.image.load('system_resources\\hard_drive.png').convert_alpha()
        self.system_images['hard_drive_offline'] = pygame.image.load('system_resources\\hard_drive_offline.png').convert_alpha()
        self.system_images['datasets_only'] = pygame.image.load('system_resources\\datasets_only.png').convert_alpha()
        self.system_images['datasets_only_offline'] = pygame.image.load('system_resources\\datasets_only_offline.png').convert_alpha()
        
    #sensitivity analysis
        self.system_images['sensitivity_analysis_view_rates'] = pygame.image.load('system_resources\\sensitivity_analysis_view_rates.png').convert_alpha()
        self.system_images['sensitivity_analysis_view_species'] = pygame.image.load('system_resources\\sensitivity_analysis_view_species.png').convert_alpha()
        self.system_images['plot_icon'] = pygame.image.load('system_resources\\plot_icon.png').convert_alpha()
        self.system_images['timeline'] = pygame.image.load('system_resources\\timeline.png').convert_alpha()
        self.system_images['time_control'] = pygame.image.load('system_resources\\time_control.png').convert_alpha()
        self.system_images['initial_time_control'] = pygame.image.load('system_resources\\initial_time_control.png').convert_alpha()
        self.system_images['positive_perturbation'] = pygame.image.load('system_resources\\positive_perturbation.png').convert_alpha()
        self.system_images['negative_perturbation'] = pygame.image.load('system_resources\\negative_perturbation.png').convert_alpha()
        self.system_images['perturbation_multiply'] = pygame.image.load('system_resources\\perturbation_multiply.png').convert_alpha()
        self.system_images['perturbation_divide'] = pygame.image.load('system_resources\\perturbation_divide.png').convert_alpha()
        self.system_images['heatmap_icon'] = pygame.image.load('system_resources\\heatmap_icon.png').convert_alpha()
        self.system_images['no_heatmap_icon'] = pygame.image.load('system_resources\\no_heatmap_icon.png').convert_alpha()
        self.system_images['heatmap_number_icon'] = pygame.image.load('system_resources\\heatmap_number_icon.png').convert_alpha()
        
    # stochastic simulation
        self.system_images['conversion_enabled'] = pygame.image.load('system_resources\\conversion_enabled.png').convert_alpha()
        self.system_images['conversion_disabled'] = pygame.image.load('system_resources\\conversion_disabled.png').convert_alpha()
        self.system_images['tauleaping_enabled'] = pygame.image.load('system_resources\\tauleaping_enabled.png').convert_alpha()
        self.system_images['tauleaping_disabled'] = pygame.image.load('system_resources\\tauleaping_disabled.png').convert_alpha()
    
    # michaelis menten
        self.system_images['michaelis_menten_reaction'] = pygame.image.load('system_resources\\michaelis_menten_reaction.png').convert_alpha()
        self.system_images['species_small'] = pygame.image.load('system_resources\\species_small.png').convert_alpha()
        self.system_images['select_species_background'] = pygame.image.load('system_resources\\select_species_background.png').convert_alpha()
        self.system_images['start_analysis'] = pygame.image.load('system_resources\\start_analysis.png').convert_alpha()
        self.system_images['michaelis_menten_results'] = pygame.image.load('system_resources\\michaelis_menten_results.png').convert_alpha()
        self.system_images['equation_fitted'] = pygame.image.load('system_resources\\equation_fitted.png').convert_alpha()
        self.system_images['vmax_equation'] = pygame.image.load('system_resources\\vmax_equation.png').convert_alpha()

    #icons 
        self.system_images['link_break'] = pygame.image.load('system_resources\\link_break.png').convert_alpha()
        self.system_images['link_add'] = pygame.image.load('system_resources\\link_add.png').convert_alpha()
        self.system_images['add_icon'] = pygame.image.load('system_resources\\add_icon.png').convert_alpha()
        self.system_images['save_icon'] = pygame.image.load('system_resources\\save_icon.png').convert_alpha()
        self.system_images['save_sideways_icon'] = pygame.image.load('system_resources\\save_sideways_icon.png').convert_alpha()
        self.system_images['trashcan'] = pygame.image.load('system_resources\\trashcan.png').convert_alpha()
        self.system_images['trashcan_confirm'] = pygame.image.load('system_resources\\trashcan_confirm.png').convert_alpha()
        self.system_images['accept'] = pygame.image.load('system_resources\\accept.png').convert_alpha()
        self.system_images['cross'] = pygame.image.load('system_resources\\cross.png').convert_alpha()
        self.system_images['edit'] = pygame.image.load('system_resources\\page_white_edit.png').convert_alpha()
        self.system_images['copy'] = pygame.image.load('system_resources\\copy.png').convert_alpha()
        self.system_images['lock_closed_off'] = pygame.image.load('system_resources\lock_closed_off.png').convert_alpha()
        self.system_images['lock_closed'] = pygame.image.load('system_resources\lock_closed.png').convert_alpha()
        self.system_images['lock_open'] = pygame.image.load('system_resources\\lock_open.png').convert_alpha()
        self.system_images['instantaneous_on'] = pygame.image.load('system_resources\\instantaneous.png').convert_alpha()
        self.system_images['instantaneous_off'] = pygame.image.load('system_resources\\instantaneous_off.png').convert_alpha()
        self.system_images['liposome_on'] = pygame.image.load('system_resources\\liposome_on.png').convert_alpha()
        self.system_images['liposome_off'] = pygame.image.load('system_resources\\liposome_off.png').convert_alpha()
        self.system_images['load_db'] = pygame.image.load('system_resources\\load_db.png').convert_alpha()
        self.system_images['table_icon'] = pygame.image.load('system_resources\\table.png').convert_alpha()
        self.system_images['add_plot'] = pygame.image.load('system_resources\\add_plot.png').convert_alpha()
        self.system_images['add_dataset'] = pygame.image.load('system_resources\\drive_add.png').convert_alpha()
        self.system_images['add_to_plot'] = pygame.image.load('system_resources\\add_to_plot.png').convert_alpha()
        self.system_images['pop_out'] = pygame.image.load('system_resources\\pop_out.png').convert_alpha()
        self.system_images['visible_icon'] = pygame.image.load('system_resources\\visible_icon.png').convert_alpha()
        self.system_images['invisible_icon'] = pygame.image.load('system_resources\\invisible_icon.png').convert_alpha()
        self.system_images['all_visible_icon'] = pygame.image.load('system_resources\\all_visible_icon.png').convert_alpha()
        self.system_images['all_invisible_icon'] = pygame.image.load('system_resources\\all_invisible_icon.png').convert_alpha()
        self.system_images['rename_icon'] = pygame.image.load('system_resources\\rename_icon.png').convert_alpha()
        
        self.system_images['checkbox_unchecked'] = pygame.image.load('system_resources\\checkbox_unchecked.png').convert_alpha()
        self.system_images['checkbox_checked'] = pygame.image.load('system_resources\\checkbox_checked.png').convert_alpha()
        
        self.system_images['variance_disabled'] = pygame.image.load('system_resources\\variance_disabled.png').convert_alpha()
        self.system_images['std_disabled'] = pygame.image.load('system_resources\\std_disabled.png').convert_alpha()
        self.system_images['fano_disabled'] = pygame.image.load('system_resources\\fano_disabled.png').convert_alpha()
        self.system_images['otherplots_disabled'] = pygame.image.load('system_resources\\otherplots_disabled.png').convert_alpha()
        
        self.system_images['variance_enabled'] = pygame.image.load('system_resources\\variance_enabled.png').convert_alpha()
        self.system_images['std_enabled'] = pygame.image.load('system_resources\\std_enabled.png').convert_alpha()
        self.system_images['fano_enabled'] = pygame.image.load('system_resources\\fano_enabled.png').convert_alpha()
        self.system_images['otherplots_enabled'] = pygame.image.load('system_resources\\otherplots_enabled.png').convert_alpha()
        
        self.system_images['variance_enabled_aside'] = pygame.image.load('system_resources\\variance_enabled_aside.png').convert_alpha()
        self.system_images['std_enabled_aside'] = pygame.image.load('system_resources\\std_enabled_aside.png').convert_alpha()
        self.system_images['fano_enabled_aside'] = pygame.image.load('system_resources\\fano_enabled_aside.png').convert_alpha()
        
        self.system_images['deterministic_icon_big_offline'] = pygame.image.load('system_resources\\deterministic_icon_big_offline.png').convert_alpha()
        self.system_images['stochastic_icon_big_offline'] = pygame.image.load('system_resources\\stochastic_icon_big_offline.png').convert_alpha()
        self.system_images['deterministic_icon_big'] = pygame.image.load('system_resources\\deterministic_icon_big.png').convert_alpha()
        self.system_images['stochastic_icon_big'] = pygame.image.load('system_resources\\stochastic_icon_big.png').convert_alpha()
        
        self.system_images_loaded = True
        
    def getImages(self):
        return self.system_images
    
    def getStatus(self):
        return self.system_images_loaded


class genLink():
    
    def __init__(self,x_override=-1,y_override=-1):
        self.x_override = x_override
        self.y_override = y_override

    def initGUI(self):
        global notification_center
        self.checkFolders()
        
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.font = []
        self.frametimes_deck = []
        self.notification_center = []
        self.notification_time_start = 0
        
        self.system_images = {}
        
        self.system_images_loaded = False         
        self.last_lookup = ''
        self.showScreenSpace_on = False
        self.alignmentTools_on = False
        self.mouse_pressed_xy = [0,0]
        
        self.x = 1680
        self.y = 1050
        
        fullscreen = FULLSCREEN
        
        #override settings
#         fullscreen = False
        
        if self.x_override != -1 and self.y_override != -1:
            fullscreen = False
            self.x = self.x_override
            self.y = self.y_override
        
        if not fullscreen:
            self.screen = pygame.display.set_mode((self.x,self.y))
        else:
            self.screen = pygame.display.set_mode((self.x,self.y),pygame.FULLSCREEN)
        
        self.loadSystemImagesThreaded()
        
        pygame.display.set_caption('GenLink')
        icon = pygame.image.load('system_resources\\icon.png')
        pygame.display.set_icon(icon) #load icon
        
        self.selected_item_id = ''
        self.selected_table = "none"
        self.time_clicked = 0
        
        self.shift_on,self.control_on,self.alt_on = False,False,False
        
        fontname = "system_resources\\fonts\\verdana.ttf"
        self.font.append(pygame.font.Font(fontname,9)) #0
        self.font.append(pygame.font.Font(fontname,12))#1
        self.font.append(pygame.font.Font(fontname,14))#2
        self.font.append(pygame.font.Font(fontname,16))#3
        self.font.append(pygame.font.Font(fontname,18))#4
        self.font.append(pygame.font.Font(fontname,20))#5
        self.font.append(pygame.font.Font(fontname,22))#6
        self.font.append(pygame.font.Font(fontname,25))#7
        self.font.append(pygame.font.Font(fontname,35))#8
        self.font.append(pygame.font.Font(fontname,75))#9
        
        
        fontname = "system_resources\\fonts\\TrajanPro-Bold.otf"
        self.font.append(pygame.font.Font(fontname,9)) #0
        self.font.append(pygame.font.Font(fontname,12))#1
        self.font.append(pygame.font.Font(fontname,14))#2
        self.font.append(pygame.font.Font(fontname,16))#3
        self.font.append(pygame.font.Font(fontname,18))#4
        self.font.append(pygame.font.Font(fontname,20))#5
        self.font.append(pygame.font.Font(fontname,22))#6
        self.font.append(pygame.font.Font(fontname,25))#7
        self.font.append(pygame.font.Font(fontname,35))#8
        self.font.append(pygame.font.Font(fontname,75))#9)
              
    def checkFolders(self):
        if os.path.exists("databases") == False:
            os.mkdir("databases") 
            print "databases folder not found, creating.."
        if os.path.exists("experimental_data") == False:
            os.mkdir("experimental_data")
            print "experimental_data folder not found, creating.." 
        if os.path.exists("export") == False:
            os.mkdir("export") 
            print "export folder not found, creating.."
        if os.path.exists("sensitivity_analysis") == False:
            os.mkdir("sensitivity_analysis") 
            print "sensitivity_analysis folder not found, creating.."
        if os.path.exists("simulation_results") == False:
            os.mkdir("simulation_results") 
            print "simulation_results folder not found, creating.."
        if os.path.exists("simulation_results/deterministic") == False:
            os.mkdir("simulation_results/deterministic") 
            print "simulation_results/deterministic folder not found, creating.."
        if os.path.exists("simulation_results/stochastic") == False:
            os.mkdir("simulation_results/stochastic") 
            print "simulation_results/stochastic folder not found, creating.."
        if os.path.exists("system_resources") == False:
            os.mkdir("system_resources") 
            print "system_resources folder not found, creating.."
        if os.path.exists("system_resources/fonts") == False:
            os.mkdir("system_resources/fonts") 
            print "system_resources/fonts folder not found, creating.."
        if os.path.exists("fitting_data") == False:
            os.mkdir("fitting_data") 
            print "fitting_data folder not found, creating.."
        if os.path.exists("screenshots") == False:
            os.mkdir("screenshots") 
            print "screenshots folder not found, creating.."    
                  
    def previewPlotColors(self, commented_line_success):
        self.running = True
        showScreenSpace_on = False
        
        pygame.event.set_blocked(MOUSEMOTION)
        self.resetFields()
        while self.running:
            self.screenspace = {}
            if self.running:
                
                amount_of_colors = len(PLOT_COLORS)
                x = self.x / math.floor(amount_of_colors/2)
                y = (self.y-50) / 2
                
                y_index = 0
                x_index = 0
                for i in range(amount_of_colors):
                    self.screen.blit(getBlock(x,y,(PLOT_COLORS[i])),(x_index*x,y_index*y))
                    self.writetext(str(i+1),4,x_index*x+2,y_index*y+5)
                    self.writetext(str(PLOT_COLORS[i][0]) + "," +str(PLOT_COLORS[i][1]) + "," +str(PLOT_COLORS[i][2]),0,x_index*x+2,y_index*y+20)
                    
                    if i == math.floor(amount_of_colors/2):
                        y_index += 1
                        x_index = -1
                
                    x_index += 1    
                    
                if showScreenSpace_on:
                    self.showScreenSpace()  
                
                self.screen.blit(getBlock(self.x,50,(255,255,255,255)),(0,self.y-50))
                if commented_line_success:
                    self.writetext("STATUS OF ALTERING MATPLOTLIB FILE: success",3,10,self.y-35,color=(20,20,20))
                else:
                    self.writetext("STATUS OF ALTERING MATPLOTLIB FILE: FAILED!.",3,10,self.y-35,color=(20,20,20))
                    self.writetext("The screen may flicker when a graph is plotted... Manually comment out line 97 of matplotlib.backends.backend_tkagg",2,10,self.y-20,color=(20,20,20))
                pygame.time.wait(25) #saves cpu time
                pygame.display.flip()#refresh the screen
                
                #this checks the events of the program
                self.checkEvents()
        pygame.quit()
    
    def storeDB(self,table):
        storeDB_thread = storeDB(table)
        storeDB_thread.setDaemon = True
        storeDB_thread.start()
            
    def splitToLines(self,string,max_length,max_lines):
        new_string = ''
        string = str(string)
        lines = []
        if len(string) >= max_length:
            word_array = string.split(' ')
            for index,word in enumerate(word_array):
                if word == '\n':
                    lines.append(new_string.strip()) 
                    new_string = ''
                else:
                    new_string = new_string + " " + word
                    if len(lines) < max_lines:
                        if index+1 < len(word_array):
                            if (len(new_string)+1+len(word_array[index+1])) >= max_length:
                                lines.append(new_string.strip())
                                new_string = ''
                        else:
                            lines.append(new_string.strip()) 
                    else:
                        lines[max_lines-1] = lines[max_lines-1] + "..."
                        break
        else:
            lines.append(string)
      
        return lines 
     
    def writetext(self,input_text,size,xpos,ypos,centerx=False,centery=True,color=TEXT_DEFAULT_COLOR,max_length=1000, max_lines=2, blitTo=""):
        lines = self.splitToLines(input_text,max_length,max_lines)
        line_height = (9,12,14,16,18,20,22,25,35,75,9,12,14,16,18,20,22,25,35,75)
        for text in lines:
            text = self.font[size].render(text,1,color)
            if centerx and centery:
                text_pos = text.get_rect(centerx=xpos,centery=ypos)
            elif centerx:
                text_pos = text.get_rect(centerx=xpos,y=ypos)
            elif centery:
                text_pos = text.get_rect(x=xpos,centery=ypos)
            else:
                text_pos = text.get_rect(x=xpos,y=ypos)
            if blitTo == "":
                self.screen.blit(text,text_pos)
            else:
                blitTo.blit(text,text_pos)
            ypos = ypos+(line_height[size]+4)
        return len(lines) + 1

    def loadSystemImagesThreaded(self):
        self.imageLoader = imageLoader();
        self.imageLoader.start()
    
    def showImage(self,title,(xpos,ypos),click_id="",click_border=2,custom_screenspace=((0,0),(0,0)),clearScreenspaceBehind=False,blitTo="",blitToPos=[0,0]):
        if blitTo != "":
            blitTo.blit(self.system_images[title],(xpos,ypos))
        else:
            self.screen.blit(self.system_images[title],(xpos,ypos))
            
        if clearScreenspaceBehind:
            (width,height) = self.system_images[title].get_size()
            self.clearScreenspaceInArea(xpos,ypos,width,height)
            
        if click_id != "" and custom_screenspace == ((0,0),(0,0)):
            (width,height) = self.system_images[title].get_size() 
            blitX = blitToPos[0]
            blitY = blitToPos[1]
            
            if blitTo != "":
                self.screenspace[click_id] = ((blitX+xpos-click_border,blitY+ypos-click_border),(blitX+xpos+width+click_border,blitY+ypos+height+click_border))
            else:
                self.screenspace[click_id] = ((xpos-click_border,ypos-click_border),(xpos+width+click_border,ypos+height+click_border))
        elif click_id != "":
            self.screenspace[click_id] = custom_screenspace
    
    def clearScreenspaceInArea(self,xpos,ypos,width,height):
        new_screenspace = {} 
        for screenspace_title,space in self.screenspace.iteritems():
            if (xpos <= space[0][0] <= xpos+width or \
                xpos <= space[1][0] <= xpos+width) and \
                 (ypos <= space[0][1] <= ypos+height or \
                 ypos <= space[1][1] <= ypos+height):
                pass
            else:
                new_screenspace[screenspace_title] = space
        self.screenspace = new_screenspace
        
    def resetFields(self):
    #===The variables are defined at GUI level because they will not be saved if they are reinitiated each frame    

    # general
#        print 'Called resetFields'
        self.active_field = ""
        self.active_field_id = 0
        self.active_field_start = 0
        self.text_y = 0
        self.text_x = 0
        
    # reactions
        self.category_field = ""
        self.reaction_reactant_field = ""
        self.reaction_product_field = ""
        self.reaction_reversible = True
        self.k1_link = ""
        self.k_1_link = ""
        self.k1_unique = False
        self.k_1_unique = False
        self.k1 = ""
        self.k_1 = ""
        self.keq = ""
        self.constrains = ""
        self.linking_value = ""
        self.edit_initial_amount = ''
        self.initial_amount_index = 1
        self.editing_id = -1
        self.instantaneous = "off"
        self.rate_unit_order = ""
        self.k_1_times_1_over_volume = 0
        self.k1_times_1_over_volume = 0
        self.reaction_preview = False
        self.plotted_preview = False
        self.copying_reaction = False
        
    # species
        self.edit_artificial_species_id = '-1'
        self.artificial_species_popup = False
        self.converting_to_artificial = False
        self.artificial_species_name = ""
        self.artificial_species_operation_type = 0
        self.artificial_species_operateIDs = []
        self.species_change_volume = "0"
        self.volume_in_liposome = "no"
        self.scroll_surface = ""
        
    # for deterministic simulation
        self.initializeSim = 0
        self.plot_species = []
        self.deterministic_total_time = ''
        self.deterministic_reporter_interval = ''
        self.error_message = ""
        self.sent_to_results = ""
        self.progress1 = 0
        self.progress2 = 0
        self.progress3 = 0
        self.status_text = ''
        self.datasets_IC_to_use = []
        self.gpu_toggled_for_simulation = "no"
        
    # stochastic simulation
        self.conversion_enabled = True
        self.disable_tauLeaping = 1
        
    # plots
        self.scratch_surfaces = []
        self.plotted = 0
        
    # experimentalDatasets
        self.selected_dataFile_index = -1
        self.experimentalDataset = experimentalData_classes.experimentalData(self,db,dataID = -1)
        self.selectSpeciesListIndex = -1
        self.selectTimeViewIndex = -1
        self.data_title = ""
        self.conversionFactor = ""
        self.initial_conditions_editor = False
        self.events_editor = False
        self.noise_reduction_enabled = 0
        self.max_amount_of_datapoints = MAXIMUM_AMOUNT_OF_POINTS_FOR_DATASET
        self.columndata_array = []
        self.view_dataset_as_graphs = False
        self.allow_reduce = False
        self.allow_smooth = False
        self.allow_conversion = False
        self.initial_condition_suggestions = []
        self.prev_percentage_used = 1
        self.percentage_used = 1
        self.percentage_applied_to_all = -1
        self.selected_plots_expData = []
        
    # fitting to data
        self.datasets_to_fit = []
        self.fit_accuracy_level = 5
        self.mutation_rate = '0.1'
        self.crossover_rate = '0.1'
        self.smooth_factor = 0
        self.reduction_factor = 0
        self.fitting_started = False
        self.stop_fitting = True
        self.stopped_fitting = False
        self.fit_applied = False
        self.previous_generation = -1
        self.fitness_results = []
        self.fit_indices = []
        self.generation = 0
        self.previous_generation = 0
        self.tableSurface = ""
        self.plotClicked = -1
        self.table_data = []
        self.high_fitness = False
        self.enable_refine = 0
        self.aborted_simulation = False
        self.examining_data_from = ""
        self.fitting_method = ""
        self.selected_algorithm = 0
        self.selected_boundary_setting = 4
        self.mathematical_fitting_completed = False
        self.mathematical_fitting_result = []
        self.mathematical_fitting_message = ""
        self.treat_datasets_as_equal = True
        self.fit_algorithm_successful = False
        self.mathematical_fitting_function_evals = 0
        self.mathematical_fitting_max_function_evals = 1
        self.datasets_residue_calculation = "addition"
        self.fitness_calculation_method = 1
        
    # events
        self.species_in_event = []
        self.selected_editing_species = '-1'
        self.event_title = ""
        self.event_time = ""
        self.event_volume = ""
        self.event_id = "-1"
        self.add_events = False
        
    # database management:
        self.selected_db_name = ""
        self.new_db_name = ""
        self.old_db_name = ""
        self.create_popup = ""
        self.error_message = ""
        self.copy_database = False
        self.rename_database = False
        
    # results
        self.species_to_add_to_plot = []
        self.selected_plots = []
        self.base_selected_plots = []
        self.scratch_icon_surfaces = []
        self.shown_plot_triggers = []
        self.add_to_plot = '-1'
        self.select_dataset_for_plot = '-1'
        self.result_type = '' # deterministic or stochastic
        self.showConcentration = False
        self.create_scatterplot = False
        self.plot_dataset = False
        self.plot_dataset_with_reduced = False
        self.thumbnail_surface = ""
        
    # sensitivity analysis
        self.enable_sensitivity_analysis = 0
        self.sensitivity_perturbation = 1.50; # 50%
        self.compare_rates = False
        self.table_view = False
        self.table_max_view = True
        self.time_slider_grabbed = False
        self.initial_time_slider_grabbed = False
        self.time_selected = -1
        self.prev_time_selected = -1
        self.initial_time_selected = 0
        self.prev_initial_time_selected = -1
        self.index_selected = 0
        self.perturbation_time_offset = 0
        self.negative_perturbation = False
        self.tmp_block = ""
        self.show_heatmap_only = False
        self.hide_heatmap = False
        self.perturbation_as_percentages = True
        self.perturb_k_values_only = False
        self.heatmapLegend = ""
        self.use_absolute_operator_for_sensitivity = False
        self.use_absolute_operator_for_sensitivity_plots = True
        
    # michaelis_menten
        self.enzyme_id = '-1'
        self.substrate_id = '-1'
        self.product_id = '-1'
        self.dataset_v_values = []
        self.selected_datasets = []
        self.show_species_selection_list = False
        self.species_selection_x = 0
        self.species_selection_y = 0
        self.identify_species_subject = ""
        self.v_values = []
        self.S_values = []
        self.E_values = []
        self.result_surface = []
        self.update_plot_times = False
        self.michaelis_menten_previous_result = []
        
        
    # misc
        #settings for gestures
        self.direction = 1
        self.mouse_pressed = 0
        self.new_menu_selection = False
        self.plot_legends = []
        
        #settings for the scrollbar:
        self.grabScrollControl = False
        self.grabScrollControl_index = 0
        self.grabScrollControl_direction = 'v'
        self.previous_selected_control = ''
        self.previous_scroll_point = (0,0)
        self.y_scroll_0 = 0
        self.y_scroll_1 = 0
        self.y_scroll_2 = 0
        self.y_scroll_3 = 0
        self.y_scroll_4 = 0
        
        self.x_scroll_0 = 0
        self.x_scroll_1 = 0
        self.x_scroll_2 = 0
        self.x_scroll_3 = 0
        self.x_scroll_4 = 0
        
        #settings for the blinker
        self.text_blinker_x = 0
        self.text_blinker_size = 0
        self.time_last_blink = -1
        self.blinker_subindex = 1000
        self.subindex_active_field = ""
        self.blinker_text_fontsize = 0
        self.blink_on_time = 0.4
        self.blink_off_time = 0.3
        
        #settings for holding backspace
        self.backspace_pressed = False
        self.delete_pressed = False
        self.left_arrow_pressed = False
        self.right_arrow_pressed = False
        self.pressed_timer = 0
        self.pressed_repeat_speed = 0.1
        
        #confirm delete
        self.confirm_delete_id = -1
        self.confirm_delete = False
        self.clicked_delete_button = False
        
        # loading bar
        self.loading_time_start = 0
        self.update_time = 0
        self.unit1 = "1"
        self.unit2 = "2"
        self.datasets_used = 0
        self.old_progress = 0
                                              
    def refreshrate_deck(self,frametime): #calculate refreshrate
        if len(self.frametimes_deck) < 20:
            self.frametimes_deck.append(frametime)
        else:
            self.frametimes_deck.pop(0)
            self.frametimes_deck.append(frametime)
        average_frametime = sum(self.frametimes_deck)/len(self.frametimes_deck)
        return str(round(1/(average_frametime+1e-4),1))
        
    def showScreenSpace(self):
        for key,space in self.screenspace.iteritems(): #@UnusedVariable
            pygame.draw.rect(self.screen,(int(random.random()*255),int(random.random()*255),int(random.random()*255)),pygame.Rect(space[0][0],space[0][1],space[1][0]-space[0][0],space[1][1]-space[0][1]))
            self.writetext(key, 0, space[0][0], space[0][1], False, False, (random.random()*255,255,random.random()*255), max_length=40, max_lines=1)
    
    def showAlignmentTools(self):
        horizontal_line = getBlock(2000,1,(0,255,0,150))
        vertical_line = getBlock(1,2000,(255,0,0,150))
        self.screen.blit(horizontal_line,(0,self.mouse_pressed_xy[1]))
        self.screen.blit(horizontal_line,(0,self.mouse_pressed_xy[1]-5))
        self.screen.blit(horizontal_line,(0,self.mouse_pressed_xy[1]+5))
        self.screen.blit(vertical_line,(self.mouse_pressed_xy[0],0))
        self.screen.blit(vertical_line,(self.mouse_pressed_xy[0]+5,0))
        self.screen.blit(vertical_line,(self.mouse_pressed_xy[0]-5,0))
                          
    def blinker(self,blinker_x,blinker_y,font_size,blinker_size=2,x_offset=4,y_offset=2):  
        if font_size < 2:
            x_offset = 1
        
        text_size = 0
        if self.active_field != "":
            exec("text_size = self.font[font_size].size(self."+self.active_field+")[0]")
        self.blinker_text_fontsize = font_size
        self.text_blinker_size = text_size
        self.text_blinker_x = blinker_x+x_offset
        
        if self.subindex_active_field != self.active_field:
            self.getBlinkerSubindex()
        
        if self.blinker_subindex != -1:
            if self.active_field != "":
                exec("text_size = self.font[font_size].size(self."+self.active_field+"[:" + str(self.blinker_subindex) + "])[0]")
        else:
            if self.active_field != "":
                length_field = 0
                exec("length_field = len(self."+self.active_field+")")
                self.blinker_subindex = length_field
        
        if (time.time() - self.time_last_blink) > self.blink_on_time or (time.time() - self.time_last_blink) < self.blink_off_time:
            if self.active_field != "":
                self.writetext('|', blinker_size, blinker_x+text_size-x_offset, blinker_y-y_offset, False, True, color=(20,20,20))
                if (time.time() - self.time_last_blink) > self.blink_on_time:
                    self.time_last_blink = time.time()
                    
    def getBlinkerSubindex(self):
        total = self.text_blinker_size
        selected = self.mouse_pressed - self.text_blinker_x
        self.subindex_active_field = self.active_field
        if total != 0:
            length_field = 0
            exec("length_field = len(self."+self.active_field+")")

            if self.mouse_pressed == 0:
                selected = self.x
            
            guessed_index = 0
            if selected >= total:
                guessed_index = length_field
            
            approx_size = 0
            for i in range(length_field):
                exec("approx_size = self.font[self.blinker_text_fontsize].size(self."+self.active_field+"[:"+str(i)+"])[0]")
                if selected <= approx_size:
                    guessed_index = i
                    break
            if approx_size < selected:
                guessed_index = length_field
                
            if guessed_index > length_field:
                self.blinker_subindex = length_field
            elif guessed_index < 0:
                self.blinker_subindex = 0
            else:
                self.blinker_subindex = guessed_index
            
        else:
            self.blinker_subindex = 0
    
    def printNotifications(self):
        if len(self.notification_center) > 0:
            intro_animation_length = 0.1
            outro_animation_length = 0.15
            notification_life = min(2.5,max(len(self.notification_center[0]) * 0.05,1.4))
            xpos = self.screen.get_width()/2
            y_distance = 23
            pop_item_id = -1
            ypos = -20
            if self.notification_time_start == 0:
                self.notification_time_start = time.time()
            if self.notification_time_start > (time.time() - intro_animation_length):
                ypos = -20 + (y_distance) * ((time.time() - self.notification_time_start)/intro_animation_length)
            elif self.notification_time_start > (time.time() - notification_life - intro_animation_length):
                ypos = 3
            elif self.notification_time_start > (time.time() - intro_animation_length - notification_life - outro_animation_length):
                ypos = 3 - (y_distance) * ((time.time() - notification_life - intro_animation_length - self.notification_time_start)/outro_animation_length)
            else:
                pop_item_id = 0
                
            if len(self.notification_center)-1 > 1:
                remaining_msg = "(" + str(len(self.notification_center)-1) + " remaining) "
            else: 
                remaining_msg = ''
            
            block_width = len(self.notification_center[0])*10 + 50
            self.screen.blit(getBorderedBlock(block_width,45,(20,20,20,255),(255,219,109,255),2),(xpos-0.5*block_width,ypos-20))
            self.writetext(remaining_msg + self.notification_center[0],3,xpos, ypos, True, False, max_length=9000, max_lines=1)
            xpos = xpos + self.font[3].size(self.notification_center[0])[0]
            if pop_item_id != -1:
                self.notification_center.pop(pop_item_id)
                self.notification_time_start = 0
                
    def initiateScrollbar(self,max_scroll_distance,xpos=-1,ypos=180,max_travel_distance=-1,horizontal=False,index=0):
        # set default values
        if xpos == -1 and not horizontal:
            xpos = self.xpos - 100
        elif xpos == -1:
            xpos = 100
            
        max_scroll_distance = int(max_scroll_distance)
        
        # set default values
        if max_travel_distance == -1 and not horizontal:
            max_pos = self.y - 100
            max_travel_distance = max_pos - ypos
        elif max_travel_distance == -1:
            max_pos = self.x - 100
            max_travel_distance = max_pos - xpos
        elif horizontal:
            max_pos = xpos + max_travel_distance
        else:
            max_pos = ypos + max_travel_distance
        
        # get direction
        if horizontal:
            direction = 'x'
        else:
            direction = 'y'
            
        # get distance 
        scrolled_distance = 0
        exec("scrolled_distance = self." + direction + "_scroll_" + str(index))
        
        scroll_offset = 0
        # move if grabbed, else get pos from distance
        if self.grabScrollControl and self.grabScrollControl_index == index and self.grabScrollControl_direction == direction:
            if horizontal:
                scroll_control_position = max(xpos,min(pygame.mouse.get_pos()[0],max_pos))
                scroll_offset = -max_scroll_distance * (scroll_control_position-xpos)/float(max_travel_distance)
            else:
                scroll_control_position = max(ypos,min(pygame.mouse.get_pos()[1],max_pos))
                scroll_offset = -max_scroll_distance * (scroll_control_position-ypos)/float(max_travel_distance)
            
            if  scroll_offset < -max_scroll_distance:
                scroll_offset = -max_scroll_distance
            
            exec("self." + direction + "_scroll_" + str(index) + " = scroll_offset")
        else:
            if horizontal:
                scroll_control_position = (scrolled_distance/(-max_scroll_distance))*(max_travel_distance) + xpos
            else:
                scroll_control_position = (scrolled_distance/(-max_scroll_distance))*(max_travel_distance) + ypos
        
        # draw scroll bar control
        if horizontal:
            self.screen.blit(self.system_images['horizontal_scrollbar_control'],(scroll_control_position,ypos))
            self.screenspace['scrollbar_control__' + str(index) + "__x__" + str(max_scroll_distance) + "__" + str(random.randint(0,9000))] = ((scroll_control_position-20,ypos-10),(scroll_control_position+60,ypos+20))
        else:
            self.screen.blit(self.system_images['scrollbar_control'],(xpos,scroll_control_position))
            self.screenspace['scrollbar_control__' + str(index) + "__y__" + str(max_scroll_distance) + "__" + str(random.randint(0,9000))] = ((xpos-10,scroll_control_position-20),(xpos+50,scroll_control_position+60))
        
    def outputLoadingBar(self,x,y,count=20): #this bar is just running and running
        if self.loading_time_start == 0:
            self.loading_time_start = time.time()
        
        x = x + 24
        
        total_time = 1.2 #seconds
        progress = ((time.time() - self.loading_time_start) % total_time)/total_time;
        
        self.screen.blit(self.system_images['load_start'],(x-24,y))
        self.screen.blit(self.system_images['load_end'],(x+25*count,y))
        if progress < 0.5:
            for i in range(count):
                a = i/float(count)
                if a < progress*2:
                    self.screen.blit(self.system_images['load_unit2'],(x+25*i,y))
                else:
                    self.screen.blit(self.system_images['load_unit1'],(x+25*i,y))
        else:
            for i in range(count):
                a = i/float(count)
                if a < (progress-0.5)*2:
                    self.screen.blit(self.system_images['load_unit1'],(x+25*i,y))
                else:
                    self.screen.blit(self.system_images['load_unit2'],(x+25*i,y))
        
    def outputProgressBar(self,x,y,length,progress,second_progress=0,third_progress=0,LightSkin=False,status_text=""):  #this bar shows the progress
        if self.loading_time_start == 0 or (progress == 0 and second_progress == 1):
            self.loading_time_start = time.time()
        elif self.datasets_used == 0 and progress == 0:    
            self.loading_time_start = time.time()
            
        if self.old_progress != progress:
            self.update_time = time.time()
            
        if LightSkin:
            border = getBorderedBlock(length,25,(255,255,255,255),(20,20,20,255),2)
            bar = getBlock((progress/100.0)*(length-4),21,(0,156,255,255))        
        else:
            border = getBorderedBlock(length,25,(0,0,0,255),(255,255,255,255),2)
            bar = getBlock((progress/100.0)*(length-4),21,(255,255,255,255))        
        if self.datasets_used != 0:
            second_bar_length = ((progress/100.0)+(second_progress-1))*(length-4)/(self.datasets_used+1)
            if second_bar_length < 0:
                second_bar_length = 0
                self.loading_time_start = time.time()
            second_bar = getBlock(second_bar_length,5,(255,209,27,255))
        else:
            second_bar = getBlock((second_progress/100.0)*(length-4),5,(255,209,27,255))
            
        self.old_progress = progress
            
        third_bar = getBlock((third_progress/100.0)*(length-4),5,(27,118,255,255))
        self.screen.blit(border,(x,y))
        self.screen.blit(bar,(x+4,y+4))
        
        if second_progress != 0:
            percent_completed = round((((progress/100.0)+(second_progress-1))/float(self.datasets_used+1))*100)
        else:
            percent_completed = round(progress)
            
        time_passed = round((self.update_time - self.loading_time_start))
        total_required_time = 100*(time_passed/(percent_completed + 1e-20))
        eta_minutes = int(math.floor((total_required_time - time_passed)/60))
        eta_seconds = int(math.floor(total_required_time - time_passed - 60*eta_minutes))
        if eta_seconds < 10:
            eta_seconds = "0" + str(eta_seconds)
        else:
            eta_seconds = str(eta_seconds)
        if percent_completed != 0 and LightSkin:
            self.writetext("Estimated time left: " + str(eta_minutes) + ":" + eta_seconds,1,x,y-10,color=(20,20,20))
        elif percent_completed != 0:
            self.writetext("Estimated time left: " + str(eta_minutes) + ":" + eta_seconds,1,x,y-10,color=(255,255,255))
       
            
        if second_progress == 0 and third_progress != 0:
            self.screen.blit(third_bar,(x+4,y+4))
            self.screen.blit(second_bar,(x+4,y+9))
        else:
            self.screen.blit(second_bar,(x+4,y+4))
            self.screen.blit(third_bar,(x+4,y+9))
        
        if status_text != "":
            self.writetext(status_text,1,x+9,y+14,color=(20,20,20))
        
    def databaseCleanup(self):
    #This cleans the database to remove the orphaned k-values and species
        k = kvalues_classes.kvalue(self,db)
        k.updateKDatabase()
        s = species_classes.species(self,db)
        s.updateSpeciesDatabase()
    # Cleaning datasets
        remaining_datasets = []
        for set in db.tbl['experimental_data']:
            if os.path.exists('experimental_data'):
                files_in_dir = os.listdir('experimental_data')
            if set['filename'] in files_in_dir:
                remaining_datasets.append(set)
        db.tbl['experimental_data'] = remaining_datasets
        
    # setting orphaned reactions into uncategorized   
        reactions_changed = False 
        for reaction in db.tbl['reactions']:
            category_exists = False
            for category in db.tbl['categories']:
                if category['id'] == reaction['category']:
                    category_exists = True
                    break
            if not category_exists:
                reactions_changed = True
                reaction['category'] = '1000000'
        if reactions_changed:
            db.storeFull('reactions')
    
         
    
    def checkDefaultDBEntrees(self):
        if db.dbname != "":
            #make sure there is a volume entree
            if len(db.tbl['settings']) == 0:
                data = {}
                data['volume'] = 1
                data['volume_in_liposome'] = 'no'
                data['deterministic_time'] = ''
                data['deterministic_reporter_interval'] = ''
                data['datasets_IC_to_use'] = ''
                data['viewed_data'] = ''
                data['last_used_conversion_factors'] = ''
                data['gpu_toggled_for_simulation'] = 'yes'
                data['stochastic_time'] = ''
                data['stochastic_reporter_interval'] = ''
                data['stochastic_enable_conversion'] = 'yes'
                data['stochastic_disable_tau_leaping'] = '1'
                data['id'] = 1
                db.save('settings',data,-1)
                
            if len(db.tbl['categories']) == 0:
                data = {}
                data['category'] = "Uncategorized"
                data['id'] = 1000000
                db.save('categories',data,-1)
    
    def loadingSequence(self,start_time,loading_background,loading_background_bw,loading_button,particle,xpos_correction_1,xpos_correction_2,reverse_fade,transparency_amount,transparency_amount_background,fade_speed):
        # loading sequence
        ticks = (time.time() - start_time)*8000
        
        if reverse_fade:
            transparency_amount -= fade_speed
        else:
            transparency_amount_background += fade_speed*1.2
            transparency_amount += fade_speed
        
        if transparency_amount > 254:
            if ticks > 8000:
                reverse_fade = True
                fade_speed = 12
            transparency_amount = 255
        elif transparency_amount < 1:
            transparency_amount = 0
        
        loading_background.set_alpha(255)
        self.screen.blit(loading_background_bw,(0,0))    
        loading_background.set_alpha(min(255,transparency_amount_background))
        self.screen.blit(loading_background,(0,0))
        loading_button.set_alpha(transparency_amount)
        
        self.screen.blit(loading_button,(450,400)) 
        
        multiplier_1 = 0.04
        multiplier_2 = 0.06
        
        xpos1 = multiplier_1*ticks
        xpos2 = multiplier_2*ticks
        
        limit1,limit2 = 0,0
        
        if xpos2 > 260:
            if ticks > 8000:
                xpos2 = xpos_correction_2-xpos2
                limit2 = 260
            else:
                xpos_correction_2 = xpos2
                xpos2 = 260
        if xpos1 > 300:
            if ticks > 10000:
                xpos1 = xpos_correction_1-xpos1
                limit1 = 300
            else:
                xpos_correction_1 = xpos1
                xpos1 = 300
            
        self.screen.blit(particle,(500+xpos1+limit1,370))
        self.screen.blit(particle,(500+xpos1+limit1,481))
        
        self.screen.blit(particle,(540+xpos2+limit2,310))
        self.screen.blit(particle,(540+xpos2+limit2,541))
        
        self.screen.blit(particle,(1100-xpos1-limit1,340))
        self.screen.blit(particle,(1100-xpos1-limit1,511))
        
        self.screen.blit(particle,(1060-xpos2-limit2,280))
        self.screen.blit(particle,(1060-xpos2-limit2,571))
        
        
        
        return (xpos_correction_1,xpos_correction_2,reverse_fade,transparency_amount,transparency_amount_background,fade_speed)
        
    def run(self):
        global db, function_notifications
        
        self.checkDefaultDBEntrees()
        
        db.restoreAllBackups()
        
        self.running = True
        
        #initialization
        self.menu_selection = ""
        self.category_field = ""
        self.selected_category = ''
        self.selected_species = ''
        self.font_size = 3
        
        # scrollbar
        self.last_scroll_time = 0
        self.max_scroll_distance = 0
        
        
        showScreenSpace_on = False
        #for refreshrate
        t_start = time.time() #@UnusedVariable
        
        loading_background = pygame.image.load('system_resources\\loading_background.png').convert()
        loading_button = pygame.image.load('system_resources\\loading_resources.png').convert()
        loading_background_bw = pygame.image.load('system_resources\\loading_background_bw.png').convert()
        particle = pygame.image.load('system_resources\\loading_particle.png').convert_alpha()
        xpos_correction_1,xpos_correction_2 = 0,0
        reverse_fade = False
        transparency_amount = 100
        transparency_amount_background = 0
        fade_speed = 6
        
        pygame.event.set_blocked(MOUSEMOTION)
        self.resetFields()
        start_time = time.time() #@UnusedVariable
        while self.running:
            t0 = time.time() #@UnusedVariable
            self.screenspace = {}
            if self.running:
                if not self.system_images_loaded: 
                    self.interface = ""
                    (xpos_correction_1,xpos_correction_2,reverse_fade,transparency_amount,transparency_amount_background,fade_speed) = self.loadingSequence(start_time,
                                                                                                                             loading_background,
                                                                                                                             loading_background_bw,
                                                                                                                             loading_button,
                                                                                                                             particle,
                                                                                                                             xpos_correction_1, xpos_correction_2,
                                                                                                                             reverse_fade,
                                                                                                                             transparency_amount,
                                                                                                                             transparency_amount_background,
                                                                                                                             fade_speed)
                    pygame.display.flip()#refresh the screen
                    pygame.time.wait(20) #saves cpu time
                    if self.imageLoader.getStatus() == True:
                        self.system_images = self.imageLoader.getImages()
                        self.system_images_loaded = True
                        del self.imageLoader
#                         print "time to complete",time.time() - start_time
                    self.checkEvents()
                else:
                    if function_notifications != []:
                        self.notification_center = function_notifications
                        function_notifications = []
                        
                    if db.dbname == "":
                        self.menu_selection = "database_management"
                        
                    if not self.menu_selection:
                        self.interface = ""
                        self.screen.blit(self.system_images['menu_interface_v3'],(0,0))                     
    
                        self.writetext("Running database: " + db.dbname, 1,self.x/2, 5, True, True)
                        
                        self.screenspace['MAIN_MENU_ITEM__categories'] = ((55,150),(620,240))
                        self.screenspace['MAIN_MENU_ITEM__reactions'] = ((55,250),(620,340))
                        self.screenspace['MAIN_MENU_ITEM__events'] =  ((55,350),(620,440))
                        self.screenspace['MAIN_MENU_ITEM__database_management'] =  ((55,450),(620,540))
    
                        self.screenspace['MAIN_MENU_ITEM__loadData'] = ((960,150),(1600,240))
                        self.screenspace['MAIN_MENU_ITEM__species'] = ((960,250),(1600,340))
                        self.screenspace['MAIN_MENU_ITEM__reactionRates'] =  ((960,350),(1600,440))
                        self.screenspace['MAIN_MENU_ITEM__fittingData'] =  ((960,450),(1600,540))
                        
#                         self.screenspace['MAIN_MENU_ITEM__deterministic'] = ((495,615),(1100,705))
#                         self.screenspace['MAIN_MENU_ITEM__stochastic'] = ((495,715),(1100,805))
#                         self.screenspace['MAIN_MENU_ITEM__results'] =  ((495,815),(1100,905))
#                         self.screenspace['MAIN_MENU_ITEM__sensitivity_analysis'] =  ((495,915),(1100,1005))

                        self.screenspace['MAIN_MENU_ITEM__deterministic'] = ((215,610),(815,710))
                        self.screenspace['MAIN_MENU_ITEM__stochastic'] = ((215,710),(815,810))
                        self.screenspace['MAIN_MENU_ITEM__results'] =  ((215,810),(815,910))
                        
                        self.screenspace['MAIN_MENU_ITEM__michaelis_menten'] =  ((860,610),(1460,710))
                        self.screenspace['MAIN_MENU_ITEM__sensitivity_analysis'] =  ((860,710),(1460,810))
                        
                    elif self.menu_selection == "categories":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = category_classes.category_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "species":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0))
                        self.interface = species_classes.species_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "reactions":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = reaction_classes.reaction_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "events":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = events_classes.events_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "deterministic":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = deterministic_simulation_classes.deterministic_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == 'stochastic':
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = stochastic_simulation_classes.stochastic_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "loadData":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = experimentalData_classes.experimentalData_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "reactionRates":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = reactionRates_classes.reactionRates_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "fittingData":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = fittingData_classes.fittingData_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "results":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = results_classes.results_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "database_management":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = database_management_classes.management_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "sensitivity_analysis":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = sensitivity_analysis_classes.sensitivity_interface(self,db)
                        self.interface.init()
                    elif self.menu_selection == "michaelis_menten":
                        self.screen.blit(self.system_images[self.menu_selection + '_background'],(0,0)) 
                        self.interface = michaelis_menten_classes.michaelis_menten_interface(self,db)
                        self.interface.init()
                        
                    if self.new_menu_selection:
                        self.interface.selectInitialField()
                        self.new_menu_selection = False
                    
                    #this makes sure keeping backspace pressed down works
                    if self.backspace_pressed or self.delete_pressed or self.right_arrow_pressed or self.left_arrow_pressed:
                        if self.active_field != "":
                            if time.time() - self.pressed_timer >= self.pressed_repeat_speed:
                                self.pressed_timer = time.time()
                                if self.backspace_pressed or self.delete_pressed:
                                    if self.backspace_pressed:
                                        self.removeChar(forward=False)
                                    else:
                                        self.removeChar(forward=True)
                                else:
                                    if self.left_arrow_pressed:
                                        self.blinker_subindex -= 1
                                        if self.blinker_subindex < 0:
                                            self.blinker_subindex = 0
                                    else:
                                        self.blinker_subindex += 1
                    
#                     #=========================== REFRESH RATE ====================================
#                     frametime = time.time() - t0
#                     self.writetext(self.refreshrate_deck(frametime) + " Hz",3,self.x - 70,3,False,False,color=(255,0,0))
#                     #=============================================================================
                    
                    if self.showScreenSpace_on:
                        self.showScreenSpace()  
                    if self.alignmentTools_on:
                        self.showAlignmentTools()
                    
                    pygame.time.wait(25) #saves cpu time
                    
                    self.printNotifications()
                    pygame.display.flip()#refresh the screen
                    
                    #this checks the events of the program
                    self.checkEvents()
        pygame.quit()
                
    def scrollNearestScrollbar(self,direction,xpos,ypos):
        #scroll settings
        scroll_speed = 30
        scroll_acceleration = 20
        
        #variable initialization
        min_distance = 10000
        scroll_index = -1
        scroll_direction = 'v'
        selected_key = ""
        #finding nearest scrollbar
        for key,obj in self.screenspace.iteritems():
            if 'scrollbar_control__' in key:
                key_list = key.split("__")
                distance = math.sqrt(math.pow(xpos-obj[0][0],2) + math.pow(ypos-obj[0][1],2))
                if min_distance > distance:
                    min_distance = distance
                    scroll_direction = key_list[2]
                    scroll_index = int(key_list[1])
                    scroll_limit = int(getFloat(key_list[3]))
                    selected_key = key
        if selected_key != "":
            #once a scrollbar is selected, it will remain to be selected until the mouse moves out of the threshold area         
            threshold = 10 #area to move before the selected control is resetted
            if selected_key != self.previous_selected_control:
                if abs(self.previous_scroll_point[0]-xpos) < threshold and abs(self.previous_scroll_point[1]-ypos) < threshold:
                    #ignore changes.
                    key_list = self.previous_selected_control.split("__")
                    scroll_direction = key_list[2]
                    scroll_index = int(key_list[1])
                    scroll_limit = int(key_list[3])
                    selected_key = self.previous_selected_control
                    
            #get the current scroll offset
            scroll_offset = 0
            exec("scroll_offset = self." + scroll_direction + "_scroll_" + str(scroll_index))
            
            # apply the scrolling step, bounded by limits
            if direction == 'up':
                scroll_offset += (scroll_speed + (0.5/(time.time() - self.last_scroll_time + 0.01))*scroll_acceleration)
                if scroll_offset > 0:
                    scroll_offset = 0
            else:
                scroll_offset -= (scroll_speed + (0.5/(time.time() - self.last_scroll_time + 0.01))*scroll_acceleration)
                if scroll_offset < -scroll_limit:
                    scroll_offset = -scroll_limit 
            
            # push the new scroll offset to the gui level variable
            exec("self." + scroll_direction + "_scroll_" + str(scroll_index) + " = scroll_offset")
            
            # store which scrollbar was selected
            self.previous_selected_control = selected_key
            self.previous_scroll_point = (xpos,ypos)
            
            # reset the time for the acceleration
            self.last_scroll_time = time.time()
         
    def saveScreenshot(self):
        import datetime
        a = datetime.datetime.now()
        timestamp = str(a.replace(microsecond=0)).replace(":",".")
        if self.menu_selection == "":
            menu_selected = "main"
        else:
            menu_selected = self.menu_selection
        pygame.image.save(self.screen,"screenshots/" + menu_selected + " at " + timestamp + ".png")
        self.notification_center.append("screenshot saved!")    

    def printChar(self,character):
        if self.active_field != "":
            exec("self."+self.active_field+" = self."+self.active_field+"[:"+str(self.blinker_subindex)+"] + '"+character+"' + self."+self.active_field+"["+str(self.blinker_subindex)+":]")
            self.blinker_subindex += 1
    
    def removeChar(self,forward):
        if forward:
            exec("self."+self.active_field+" = self."+self.active_field+"[:"+str(self.blinker_subindex)+"] + self."+self.active_field+"["+str(self.blinker_subindex+1)+":]")
        else:
            if self.blinker_subindex != 0:
                exec("self."+self.active_field+" = self."+self.active_field+"[:"+str(self.blinker_subindex-1)+"] + self."+self.active_field+"["+str(self.blinker_subindex)+":]")
                self.blinker_subindex -= 1
                if self.blinker_subindex < 0:
                    self.blinker_subindex = 0
    
    def checkEvents(self): #all the keystrokes and clicks are handled here
        for event in pygame.event.get():
            if event.type == QUIT: #quit
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.shift_on:
                        print (event.pos[0],event.pos[1])
                    self.mouse_pressed = event.pos[0]
                    self.mouse_pressed_xy = [event.pos[0],event.pos[1]]
                    self.handleClickEvent(event.pos[0],event.pos[1])
                    if self.active_field != "":
                        self.subindex_active_field = ""
                elif event.button == 3:
                    if self.selected_item_id:
                        self.handleEvent('back')
                elif event.button == 4:
                    self.scrollNearestScrollbar('up',event.pos[0],event.pos[1])
                elif event.button == 5:
                    self.scrollNearestScrollbar('down',event.pos[0],event.pos[1])
                self.mouse_pos = (event.pos[0],event.pos[1])
            elif event.type == KEYDOWN: #keys pressed
                if event.key == 27: #escape
                    if self.menu_selection != "":
                        self.interface.back()
                    else:
                        self.handleEvent("quit")
                elif event.key == 308: #alt
                    self.alt_on = True 
                elif event.key == 306: #left control
                    self.control_on = True
                elif event.key == 305: #right control
                    self.control_on = True
                elif event.key == 304 or event.key == 303: #shift
                    self.shift_on = True
                elif event.key == 285: #F4
                    if self.alt_on:
                        self.running = False
                elif event.key == 276: #left arrow
                    self.left_arrow_pressed = True
                    if self.active_field != "":
                        self.blinker_subindex -= 1
                        if self.blinker_subindex < 0:
                            self.blinker_subindex = 0
                    self.pressed_timer = time.time()
                elif event.key == 275: #right arrow
                    self.right_arrow_pressed = True
                    if self.active_field != "":
                        self.blinker_subindex += 1
                    self.pressed_timer = time.time()
                elif event.key == 278: #home
                    self.blinker_subindex = 0
                elif event.key == 279: #end
                    self.mouse_pressed = 1900
                    self.getBlinkerSubindex()
                elif self.shift_on and (48 <= event.key <= 57): #numbers
                    symbols_array = ['!','@','#','$','%','^','&','*','(',')']
                    character = symbols_array[event.key - 49]
                    self.printChar(character)
                elif 48 <= event.key <= 57:     #numbers
                    character = str(event.key - 48)
                    self.printChar(character)
                elif 256 <= event.key <= 265:   #keypad
                    character = str(event.key - 256)
                    self.printChar(character)
                elif self.shift_on and event.key == 45:         #underscore
                    character = chr(95)
                    self.printChar(character)
                elif event.key == 45 or event.key == 269:       #min
                    character = '-'
                    self.printChar(character)
                elif event.key == 266:                          #keypad-dot
                    character = '.'
                    self.printChar(character)
                elif event.key == 8:            #backspace
                    if self.active_field != "":
                        self.backspace_pressed = True
                        self.removeChar(forward=False)
                        self.pressed_timer = time.time()
                elif event.key == 127: #delete
                    if self.active_field != "":
                        self.delete_pressed = True
                        self.removeChar(forward=True)
                        self.pressed_timer = time.time()
                elif (self.shift_on and event.key == 61) or event.key == 270:
                    character = str("+")
                    self.printChar(character)
                elif (32 <= event.key <= 122) and (event.key != 47) and (event.key != 92) and (event.key != 41) and (event.key != 58) and (event.key != 63) or (event.key == 62) and (event.key != 60) and (event.key != 34): #caps, letters, space'
                    if self.control_on and event.key == 115: #cntrl S --> screenspace
                        if self.showScreenSpace_on:
                            self.showScreenSpace_on = False
                        else:
                            self.showScreenSpace_on = True
                    if self.control_on and event.key == 97: #cntrl a --> alignmentTools_on
                        if self.alignmentTools_on:
                            self.alignmentTools_on = False
                        else:
                            self.alignmentTools_on = True
                    elif self.control_on and event.key == 103:
                        self.saveScreenshot()
                    elif self.active_field != "":
                        if self.control_on and event.key == 118: #cntrl v --> paste
                            r = Tkinter.Tk()
                            r.withdraw()
                            character = r.clipboard_get()
                            self.printChar(character)
                            r.destroy()
                        elif self.shift_on and (97 <= event.key <= 122): #caps
                            character = chr(event.key - 32)
                            self.printChar(character)
                        else:
                            character = chr(event.key)
                            self.printChar(character)
                elif event.key == 9:            #tab
                    if self.menu_selection != "":
                        self.interface.selectNextField()  
                elif event.key == 13 or event.key == 271: #enter or keypad enter
                    if self.menu_selection != "":
                        self.interface.pressedReturn()
                
            elif event.type == KEYUP:           #keys pressed
                if event.key == 8:              #backspace
                    self.backspace_pressed = False
                elif event.key == 127:
                    self.delete_pressed = False
                elif event.key == 304 or event.key == 303: #shift
                    self.shift_on = False
                    self.handleEvent("released_shift")
                elif event.key == 306:          #control
                    self.control_on = False
                elif event.key == 308:          #alt
                    self.alt_on = False 
                elif event.key == 276: #left arrow
                    self.left_arrow_pressed = False
                elif event.key == 275: #right arrow
                    self.right_arrow_pressed = False
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.grabScrollControl = False
                    if self.mouse_pressed != 0:
                        if abs(event.pos[0] - self.mouse_pressed) > 4: #threshold for drag
                            if event.pos[0] < self.mouse_pressed:
                                self.direction = -1
                            else:
                                self.direction = 1
                            self.mouse_pressed = 0
                            if self.interface != "": #for fitting
                                self.interface.handleEvents('set_direction')
                                self.interface.handleEvents("mouse_released__" +  str(self.mouse_pressed_xy[0]) + "__" +  str(self.mouse_pressed_xy[1]) + "__" + str(event.pos[0]) + "__" + str(event.pos[1])) 
                        else:
                            self.mouse_pressed = 0
                            if self.interface != "": #for fitting
                                self.interface.handleEvents('remove_focus')
                                self.interface.handleEvents("mouse_released__" +   str(self.mouse_pressed_xy[0]) + "__" +  str(self.mouse_pressed_xy[1]) + "__" + str(event.pos[0]) + "__" + str(event.pos[1]))
                    if self.time_slider_grabbed:
                        if self.interface != "": #for fitting
                            self.interface.handleEvents("slider_released")
                    self.time_slider_grabbed = False
                    self.initial_time_slider_grabbed = False
                                       
    def handleClickEvent(self,click_x,click_y): #finds in which screenspace you clicked
        hits = []
        self.clicked_delete_button = False
        for key,obj in self.screenspace.iteritems():
            if obj[0][0] <= click_x <= obj[1][0] and obj[0][1] <= click_y <= obj[1][1]:
                hits.append(key)
        if hits:
            self.handleEvent(hits[0]) 
        
        if not self.clicked_delete_button:
            self.confirm_delete = False           
        
    def handleEvent(self,key): #this handles all the click events...
        global db         
        key_list = key.split("__")
        if 'quit' in key:
            self.running = False
        elif 'select_category__' in key:
            if self.selected_category == key_list[1]:
                self.selected_category = ''
                self.resetFields()
            else:
                self.selected_category = key_list[1]
            self.y_scroll = 0
        elif 'MAIN_MENU_ITEM__' in key:
            self.databaseCleanup()
            self.resetFields()
            self.menu_selection = key_list[1]
            self.y_scroll = 0
            self.new_menu_selection = True
        elif 'scrollbar_control' in key:
            self.grabScrollControl = True
            self.grabScrollControl_index = int(key_list[1]) 
            self.grabScrollControl_direction = key_list[2]
        else:
            if self.interface != "":
                self.interface.handleEvents(key) 

    def selectNextField(self):
        pass

        
if __name__ == '__main__':
    a = genLink()
    a.initGUI()
    a.run()
