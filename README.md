# Pandemic and Epidemic Data Analysis

A Python script for processing and analyzing historical pandemic and epidemic data from a CSV dataset.

## Features

- **Data Loading**: Reads pandemic/epidemic data from CSV file
- **Data Cleaning**: Removes duplicates and handles missing values
- **Data Validation**: Converts data types and validates for logical consistency
- **Data Aggregation**: Groups data by pathogen type and calculates summary statistics
- **Multi-format Output**: 
  - Saves processed data to CSV file
  - Stores data in SQLite database for easy querying

## Requirements

- Python 3.7+
- pandas
- sqlite3 (included with Python)

## Installation

```bash
pip install pandas
```

## Usage

1. Place your CSV file named `Historical_Pandemic_Epidemic_Dataset.csv` in the same directory as the script
2. Run the script:

```bash
python second\ Skript\(simple\).py
```

## Output

The script generates:

1. **summary_by_pathogen.csv** - Summary statistics grouped by pathogen type:
   - Total deaths
   - Total cases
   - Average case fatality rate
   - Number of events
   - Death percentage

2. **pandemic_data.db** - SQLite database containing:
   - `raw_pandemics` table - Processed raw data
   - `summary_by_pathogen` table - Summary statistics

## Sample Output

```
✅ Data loaded and processed successfully

General statistics:
Total events: [number]
Total deaths: [number]
Total cases: [number]

Summary by pathogen type:
[Table with pathogen types and statistics]
```

## Data Validation Rules

- Estimated deaths must be >= 0
- Estimated cases must be >= estimated deaths
- Case fatality rate must be <= 100%
- All key fields (Pathogen_Type, Estimated_Deaths, Estimated_Cases) must be present

## License

This project is licensed under the MIT License.

## Author

Created for data analysis purposes.
