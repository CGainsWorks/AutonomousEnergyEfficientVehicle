import pandas as pd

def error_analysis_sleep_modes(file_path):
    df = pd.read_csv(file_path)

    # Convert to numeric and filter for valid modes
    df[['Power (mW)', 'Current (mA)', 'Voltage (V)']] = df[['Power (mW)', 'Current (mA)', 'Voltage (V)']].apply(pd.to_numeric, errors='coerce')
    valid_modes = ['POWER', 'LIGHT_SLEEP', 'DEEP_SLEEP']
    df_filtered = df[df['Mode'].isin(valid_modes)]
    df_cleaned = df_filtered.dropna(subset=['Power (mW)', 'Current (mA)', 'Voltage (V)'])

    # Analysis for each mode
    results = {}
    for mode, group in df_cleaned.groupby('Mode'):
        means = group[['Power (mW)', 'Current (mA)', 'Voltage (V)']].mean()
        stds = group[['Power (mW)', 'Current (mA)', 'Voltage (V)']].std()

        # Calculate power from mean V and I
        power_mean_calc = means['Voltage (V)'] * means['Current (mA)']

        # Error propagation for power calculation
        power_error_calc = power_mean_calc * ((stds['Voltage (V)'] / means['Voltage (V)'])**2 + (stds['Current (mA)'] / means['Current (mA)'])**2)**0.5

        results[mode] = {
            'Means': means,
            'Standard Deviations': stds,
            'Calculated Power Mean': power_mean_calc,
            'Calculated Power Error': power_error_calc
        }

    return results

# Example usage:
sleep_error_analysis = error_analysis_sleep_modes("power_measurements_sleepmodes.csv")

print("Sleep Modes Error Analysis:")
for mode, analysis in sleep_error_analysis.items():
    print(f"\nMode: {mode}")
    print(f"Means:\n{analysis['Means']}")
    print(f"Standard Deviations:\n{analysis['Standard Deviations']}")
    print(f"Calculated Power Mean: {analysis['Calculated Power Mean']:.3f} mW")
    print(f"Calculated Power Error: ±{analysis['Calculated Power Error']:.3f} mW")
