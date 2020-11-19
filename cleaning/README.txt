Cleaning
1. Delete matching products from each retailer if all columns match 
- OpenRefine: (facet wm_ID, select duplicated ID, edit cells-blank down (name column), column-text facet, select (blank), all-edit rows-remove matching rows)
2. Combine products with the same wm_ID (OpenRefine)
- OpenRefine: (column text facet - cluster - Method:'nearest neighbor', ppm)

3. Flatten feat_labels, feat_values 
- Python
4. Remove product if name includes 'refurbished' / 'used' / 'refurbish' 
- Python
5. Extract product information from 'about'/'description'
- Python
6. Remove decorative strings from attributes; ie. remove uninformative text 
- Python

7. Combine datasets across retailers 
- MySQL: Union products
- OpenRefine (facet): Combine products
- Calculate rating
- Feature aggregation

8. Remove unqualified rows: products with no rating 
- Excel: filter, copy data to a different sheet, create a new csv file

---------------------------------------------------------------------------------------------------------
THIS SCRIPT TAKES CARE OF STEP 3-7.
COMPLETE STEP 1 AND BEFORE MOVING TO PYTHON
INSTRUCTION FOR THIS SCRIPT:
1. Open your IDE (spyder, etc.)

- Tailor the following parameters to fit your dataset
2. Open 'parameters_by_retailer.py'
3. Change values of colnames to fit your data column names
	- 'COLNAME_RETIALER_ID': Change if you have a retailer specific ID (eg. walmart ID, ASIN)
	- 'COLNAME_LABELS' and 'COLNAME_VALUES'
	- if there is a list feature ('[...]') such as 'feat_labels', 'feat_values' in walmart and bhphotovideo: change colnames
	- else: change values of 'COLNAME_LABELS' and 'COLNAME_VALUES' to empty string ''
4. Adjust 'features_re'
5. Open 'execute_cleaning.py'
6. Change your 'path'(working directory = path\cleaning), 'data_path', and 'retailer'
7. Change the other parameters 'factorize_...', 'numeric_columns', ...

- Run 'execute_cleaning.py'
8. run 'execute_cleaning.py'; This will save a new csv to your path called 'products_cleaned+time.csv'
9. Go to your working directory (/cleaning), change the new csv name to 'products_cleaned.csv'

- Remove extra columns
10. open 'remove_extra_columns.py'
11. Change 'col_remove' to columns you wish to remove from your specific dataset (columns that don't contribute to feature analysis)
12. run 'remove_extra_columns.py'; This will save a csv to path called 'products_cleaned_colremoved+time.csv'

---------------------------------------------------------------------------------------------------------
Amazon - Beca
Bestbuy - Karen
BHphotovideo - Melanie
Walmart - Yicheng
Newegg - Yicheng

---------------------------------------------------------------------------------------------------------
TODO
1. Combine columns
2. Weight: unit / how to define 'lightweight'?
3. Imporve brand, mfrID extraction
4. Improve cross-retailer compatibility
5. Clean code
