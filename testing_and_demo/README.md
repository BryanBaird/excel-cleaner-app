# Resources for testing and demoing

Since this application is meant to parse and clean Excel files, it helps to have an example of the type of file it works best with!

The file `Example Complex Excel Scheet.xlsx` can be used to upload and go through the application step-by-step, or even to power automated testing.

It contains the following features that are meant to be representative of "wide" Excel spreadsheets often seen in the wild:

 - A complex multi-index, split over multiple columns
   - Basic "year" and "month" for time series
   - But also nested categories of other indices as well, in this case "Layer 1/2/3"
 - Extraneous formatting
   - Fonts, colors, bolding, alignment, lines, etc. that affect visual presentation but not the data itself
   - Merged cells
   - Sparsely populated header rows above the "true" beginning of the tabular data
   - Incomplete and unlabeled "total" rows at the bottom of the sheet, below the tabular data
   - Extraneous footnote text below the tabular data
 - Multiple types of data discrepancies that could be detected (though this detection is not yet implemented):
   - Some values missing at random
   - Some indexed rows missing entirely, including clusters based on one part of the index
   - Some Value columns that are entirely missing
   - Some values that are not clear in the data type (`-`, `N/A`, and `Null` all used for blank)
   - "Fat finger" outliers, where one value is dramatically higher than most others within that column or row
   - Data typo errors, where errant punctuation has been added to a numerical value
   - Rare negative values as another type of outlier

Note that the handling of most of these data issue types is not yet implemented, and may even not be handled within this application.