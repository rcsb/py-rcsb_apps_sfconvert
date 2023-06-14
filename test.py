from resolutioncalculator import ResolutionCalculator as RC

# Create a new instance of the ResolutionCalculator class
calculator = RC()
h = 1
k = 1
l = 1
rcell = [1.23, 1.23, 1.23, 90.0, 90.0, 90.0] # Just an example values
resol = calculator.get_resolution(h, k, l, rcell)
print(f"Resolution: {resol}")

resol = [0]
calculator.check_sf(0, resol)
