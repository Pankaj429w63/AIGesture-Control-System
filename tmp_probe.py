import importlib
m = importlib.import_module('mediapipe.tasks.python.vision.hand_landmarker')
print('module', m)
print([n for n in dir(m) if 'Landmarker' in n or 'Hand' in n or 'Landmark' in n])
print('module file', getattr(m,'__file__',None))
