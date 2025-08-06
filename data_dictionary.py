
def S2M_study():
        sujet_to_list_task = {
                "Sujet_000": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                "Sujet_001": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair", "17-hand-to-back"],
                "Sujet_002": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_001", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "Sujet_003": ["01-eat-yoghurt", "02-cut-food", "13-playdoe_002", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "Sujet_007": ["01-eat-yoghurt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "Sujet_008": ["00-static-stand","01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "Sujet_009": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "Sujet_010": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "Sujet_011": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "Sujet_012": ["01-eat-yaourt", "02-cut-food"],
                "Sujet_013": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "Sujet_014": ["01-eat-yaourt", "02-cut-food", "13-playdoe", "06-drawing", "16-comb-hair","17-hand-to-back"],
                "fake_008": ["extrinsics"],
                }
        subject_to_fq_file_video = {"Sujet_000": 120, "Sujet_001": 60,
                                    "Sujet_002": 60, "Sujet_003": 60,
                                    "Sujet_007": 60, "Sujet_008": 60,
                                    "Sujet_009": 60, "Sujet_010": 60,
                                    "Sujet_011": 60, "Sujet_012": 60,
                                    "Sujet_013": 60, "Sujet_014": 60}
        study = dict()
        study["task"] = sujet_to_list_task
        study["fq_video"] = subject_to_fq_file_video

        return study


def CRME_full_study():
        sujet_to_list_task = {
                "Subject_01_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_02_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_03_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_04_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_05_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_06_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_07_CP":["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_08_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_09_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_10_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],                                                                                                 
                "Subject_01_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_02_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation_001",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_03_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight_000"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension_000",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit"],
                "Subject_04_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction_000","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation_000","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation_000",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                 
                                  "19_Cymbals_000"],
                "Subject_05_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_06_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_07_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                 
                                  "19_Cymbals"],
                "Subject_08_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                 "Subject_09_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_10_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food_000","17_Open_Kit",                                  
                                  "19_Cymbals"],
                "Subject_11_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "03_Shoulder_Rotation","04_Elbow_Pronosupination_Bras_Straight"
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "07_Hand_to_Bottom","08_Tray","09_Static_Sit","10_Open_Box",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",
                                  "14_Eat_Yogurt","15_Playdoe","16_Cut_Food","17_Open_Kit",                                
                                  "19_Cymbals"]}
        # check to do for subject above 05
        subject_to_fq_file_video = {"Subject_01_CP": 60, "Subject_02_CP": 60,
                                    "Subject_03_CP": 60, "Subject_04_CP": 60,
                                    "Subject_05_CP": 60,"Subject_06_CP": 60, 
                                    "Subject_07_CP": 60, "Subject_08_CP": 60,
                                    "Subject_09_CP": 60, "Subject_10_CP": 60, 
                                    "Subject_01_TDC": 60,"Subject_02_TDC": 60,
                                    "Subject_03_TDC": 60,"Subject_04_TDC": 60,
                                    "Subject_05_TDC": 60,"Subject_06_TDC": 60,
                                    "Subject_07_TDC": 60,"Subject_08_TDC": 60,
                                    "Subject_09_TDC": 60,"Subject_09_TDC": 60,"Subject_10_TDC": 60}
                                    
        study = dict()
        study["task"] = sujet_to_list_task
        study["fq_video"] = subject_to_fq_file_video
        return study

def CRME_study():
        sujet_to_list_task = {
                "Subject_01_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_02_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_03_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_04_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_05_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_06_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_07_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_08_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_09_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_10_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],                                                                                                 
                "Subject_01_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_02_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation_001",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_03_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension_000",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour"],
                "Subject_04_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction_000","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation_000",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals_000"],
                "Subject_05_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_06_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_07_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_08_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                 "Subject_09_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_10_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_11_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"]}
        # check to do for subject above 05
        subject_to_fq_file_video = {"Subject_01_CP": 60, "Subject_02_CP": 60,
                                    "Subject_03_CP": 60, "Subject_04_CP": 60,
                                    "Subject_05_CP": 60,"Subject_06_CP": 60, 
                                    "Subject_07_CP": 60, "Subject_08_CP": 60,
                                    "Subject_09_CP": 60, "Subject_10_CP": 60, 
                                    "Subject_01_TDC": 60,"Subject_02_TDC": 60,
                                    "Subject_03_TDC": 60,"Subject_04_TDC": 60,
                                    "Subject_05_TDC": 60,"Subject_06_TDC": 60,
                                    "Subject_07_TDC": 60,"Subject_08_TDC": 60,
                                    "Subject_09_TDC": 60,"Subject_09_TDC": 60,"Subject_10_TDC": 60}
                                    
        study = dict()
        study["task"] = sujet_to_list_task
        study["fq_video"] = subject_to_fq_file_video
        return study


def CRME_study_ACFAS():
        # Subject_03 no open bottle because missing marker on hand
        sujet_to_list_task = {
                "Subject_01_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_02_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_03_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_04_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_05_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_06_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_07_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_08_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"], 
                "Subject_09_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_10_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],                                                                      
                "Subject_01_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_02_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation_001",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_03_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension_000",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                 ],
                "Subject_04_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction_000","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation_000",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals_000"],
                "Subject_05_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_06_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_07_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_08_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_09_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_11_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],}
        # check to do for subject above 05
        subject_to_fq_file_video = {"Subject_01_CP": 60, "Subject_02_CP": 60,
                                    "Subject_03_CP": 60, "Subject_04_CP": 60,
                                    "Subject_05_CP": 60,"Subject_06_CP": 60, 
                                    "Subject_07_CP": 60, "Subject_08_CP": 60, 
                                    "Subject_01_TDC": 60,"Subject_02_TDC": 60,
                                    "Subject_03_TDC": 60,"Subject_04_TDC": 60,
                                    "Subject_05_TDC": 60,"Subject_06_TDC": 60,
                                    "Subject_07_TDC": 60,"Subject_08_TDC": 60}
                                    
        study = dict()
        study["task"] = sujet_to_list_task
        study["fq_video"] = subject_to_fq_file_video

        return study


def CRME_study_ISB():
        # Subject_03 no open bottle because missing marker on hand
        sujet_to_list_task = {
                "Subject_01_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_02_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_03_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_04_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_05_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_06_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_07_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_08_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"], 
                "Subject_09_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_10_CP": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],                                                                      
                "Subject_01_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_02_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation_001",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_03_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension_000",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                 ],
                "Subject_04_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction_000","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation_000",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals_000"],
                "Subject_05_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_06_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour",],
                "Subject_07_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_08_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_09_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],
                "Subject_11_TDC": ["00_Static_Stand","01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                  "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                  "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                  "13_Open_a_Bottle_and_Pour","19_Cymbals"],}
        # check to do for subject above 05
        subject_to_fq_file_video = {"Subject_01_CP": 60, "Subject_02_CP": 60,
                                    "Subject_03_CP": 60, "Subject_04_CP": 60,
                                    "Subject_05_CP": 60,"Subject_06_CP": 60, 
                                    "Subject_07_CP": 60, "Subject_08_CP": 60,
                                    "Subject_09_CP": 60, "Subject_10_CP": 60, 
                                    "Subject_01_TDC": 60,"Subject_02_TDC": 60,
                                    "Subject_03_TDC": 60,"Subject_04_TDC": 60,
                                    "Subject_05_TDC": 60,"Subject_06_TDC": 60,
                                    "Subject_07_TDC": 60,"Subject_08_TDC": 60,
                                    "Subject_09_TDC": 60,"Subject_09_TDC": 60,
                                    "Subject_10_TDC": 60,"Subject_11_TDC": 60}
                                    
        study = dict()
        study["task"] = sujet_to_list_task
        study["fq_video"] = subject_to_fq_file_video

        return study


def LBMC_study():
        sujet_to_list_task = {
                "subject01": ["static","walk"],
                "subject02": ["static","walk"],
                "subject03": ["static","walk"],
                "subject04": ["static","walk"],
                "subject06": ["static","walk"],
                "subject07": ["static","walk"],
                "subject08": ["static","walk"],
                "subject09": ["static","walk"],
                "subject10": ["static","walk"],
                "subject11": ["static","walk"],
                "subject12": ["static","walk"],
                "subject13": ["static","walk"],
                "subject14": ["static","walk"],
                "subject15": ["static","walk"],
                "subject16": ["static","walk"],}
        subject_to_fq_file_video = {"subject01": 60, "subject02": 60,
                                        "subject03": 60, "subject04": 60,
                                        "subject06": 60,"subject07": 60, 
                                        "subject08": 60, "subject09": 60, 
                                        "subject10": 60,"subject11": 60,
                                        "subject12": 60,"subject13": 60,
                                        "subject14": 60,"subject15": 60,
                                        "subject16": 60}
        study = dict()
        study["task"] = sujet_to_list_task
        study["fq_video"] = subject_to_fq_file_video

        return study

def trotinette_study():
        sujet_to_list_task = {
                        "Sujet_00": ["collisiontrot_1", "collisiontrot_2", "collisiontrot_3",
                                     "deseqfronttrot_1", "deseqfronttrot_2", "deseqfronttrot_3",
                                     "deseqlattrot_1", "deseqlattrot_2", "deseqlattrot_3",
                                          "plongeon_1", "plongeon_2", "plongeon_3"],
                        "Sujet_01": ["collisiontrot_1", "collisiontrot_2", "collisiontrot_3",
                                     "deseqfronttrot_1", "deseqfronttrot_2", "deseqfronttrot_3",
                                     "deseqlattrot_1", "deseqlattrot_2", "deseqlattrot_3",
                                          "plongeon_1", "plongeon_2", "plongeon_3"],
                        }
        subject_to_fq_file_video = {"Sujet_00": 60, "Sujet_01": 60,}
        study = dict()
        study["task"] = sujet_to_list_task
        study["fq_video"] = subject_to_fq_file_video
        
        return study      

def remove_subjects(study, subjects_to_remove):
    """
    Remove subjects from the study dictionary.
    :param study: The study dictionary.
    :param subjects_to_remove: The list of subjects to remove.
    :return: The updated study dictionary.
    """
    for subject in subjects_to_remove:
        if subject in study["task"]:
            del study["task"][subject]
        if subject in study["fq_video"]:
            del study["fq_video"][subject]
    return study

def remove_tasks(study, tasks_to_remove):
        """
        Remove tasks from the study dictionary.
        :param study: The study dictionary.
        :param tasks_to_remove: The list of tasks to remove.
        :return: The updated study dictionary.
        """
        for subject in study["task"].keys():
                # Remove tasks that contain any of the substrings in tasks_to_remove
                study["task"][subject] = [
                task for task in study["task"][subject]
                if not any(substring in task for substring in tasks_to_remove)
                ]
        return study

def keep_tasks(study, tasks_to_keep):
        """
        Keep only specified tasks in the study dictionary.
        :param study: The study dictionary.
        :param tasks_to_keep: The list of tasks to keep.
        :return: The updated study dictionary.
        """
        for subject in study["task"].keys():
                # Keep only tasks that contain any of the substrings in tasks_to_keep
                study["task"][subject] = [
                task for task in study["task"][subject]
                if any(substring in task for substring in tasks_to_keep)
                ]
        return study

def keep_subjects(study, subjects_to_keep):
    """
    Keep only specified subjects in the study dictionary.
    :param study: The study dictionary.
    :param subjects_to_keep: The list of subjects to keep.
    :return: The updated study dictionary.
    """
    for subject in list(study["task"].keys()):
        if subject not in subjects_to_keep:
            del study["task"][subject]
            del study["fq_video"][subject]
    return study

if __name__ == "__main__":
    study = S2M_study()
    study = remove_subjects(study, ["Sujet_002"])
    study = remove_tasks(study, ["01", "02"])
    print(study)  # Print the updated study dictionary for verification