Cleaning

1. Delete matching products from each retailer if all columns match 
- OpenRefine: (facet wm_ID, select duplicated ID, edit cells-blank down (name column), column-text facet, select (blank), all-edit rows-remove matching rows)
2. Combine products with the same wm_ID (OpenRefine)
- OpenRefine: (column text facet - cluster - Method:'nearest neighbor', ppm)
3. Flatten feat_labels, feat_values 
- Python
4. Remove product if name includes 'refurbished' / 'used' / 'refurbish' 
- Python
5. Extract product information from 'about_text', 'about_details' 
- Python
6. Remove decorative strings from attributes; ie. remove uninformative text 
- Python
7. Combine datasets across retailers 
- MySQL: Union products
- OpenRefine (facet): Combine products
8. Remove unqualified rows: products with no rating, num_of_rating 
- Excel: filter, copy data to a different sheet, create a new csv file
