from models.WaveOptions import WaveOptionsGenerator5, WaveOptionsGenerator3

# WaveOptions for 5 fold impulsive wave
wo = WaveOptionsGenerator5(5)
print(wo.options_sorted)

wo = WaveOptionsGenerator3(10)
print(wo.options_sorted)

