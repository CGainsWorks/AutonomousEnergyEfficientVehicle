import pandas as pd

def error_analysis_pid_fuzzy(file_path):
    df = pd.read_csv(file_path)

    # Convert to numeric and drop NaN rows
    df[['Power (mW)', 'Current (mA)', 'Voltage (V)']] = df[['Power (mW)', 'Current (mA)', 'Voltage (V)']].apply(pd.to_numeric, errors='coerce')
    df_cleaned = df.dropna(subset=['Power (mW)', 'Current (mA)', 'Voltage (V)'])

    # Calculate mean and standard deviation
    means = df_cleaned[['Power (mW)', 'Current (mA)', 'Voltage (V)']].mean()
    stds = df_cleaned[['Power (mW)', 'Current (mA)', 'Voltage (V)']].std()

    # Calculate power from average V and I
    power_mean_calc = means['Voltage (V)'] * means['Current (mA)']

    # Error propagation for power calculation (P = V * I)
    power_error_calc = power_mean_calc * ((stds['Voltage (V)'] / means['Voltage (V)'])**2 + (stds['Current (mA)'] / means['Current (mA)'])**2)**0.5

    return {
        'Means': means,
        'Standard Deviations': stds,
        'Calculated Power Mean': power_mean_calc,
        'Calculated Power Error': power_error_calc
    }

# Example usage:
pid_error_analysis = error_analysis_pid_fuzzy("power_measurementsPIDPWM5min.csv")
fuzzy_error_analysis = error_analysis_pid_fuzzy("power_measurementsFUZZYPWM12min.csv")

print("PID Error Analysis:\n", pid_error_analysis)
print("\nFuzzy Error Analysis:\n", fuzzy_error_analysis)
