<script>
  import { utils } from "xlsx";
  export let trimmed_array = [];
  let trimmed_header_rows = [];
  let trimmed_trailing_rows = [];
  let detected_index_columns = [];

  $: trimmed_header_rows_count = trimmed_header_rows.length;
  $: trimmed_trailing_rows_count = trimmed_trailing_rows.length;

  export let active_sheet;
  export let parsed_original_HTML;

  const COMPLETE_COLUMNS_RATIO = 0.9;

  // TODO: Dedupe
  const DATE_COLUMN_MAPPINGS = {
    Year: "year",
    Month: "month",
    annee: "year",
    mois: "month",
    period: "date",
    periode: "date",
    date: "date",
    quarter: "quarter",
  };
  
  const CUSTOM_INDEX_COLUMN_MAPPINGS = {
    "Layer 1": "index_level_1",
    "Layer 2": "index_level_2",
    "Layer 3": "index_level_3",
  };

  const ALL_INDEX_COLUMN_MAPPINGS = {
    ...DATE_COLUMN_MAPPINGS,
    ...CUSTOM_INDEX_COLUMN_MAPPINGS,
  };

  function count_columns(dataframe) {
    return dataframe.reduce(
      (maxLen, el, i, arr) => (el.length > maxLen ? el.length : maxLen),
      0
    );
  }

  function trimHeaderRows(dataframe) {
    console.log("Here's what we're working with:");
    console.log(dataframe);
    let df = utils.sheet_to_json(dataframe, { header: 1 });
    let full_cols_count = count_columns(df);
    let COMPLETE_COLUMNS_THRESHOLD = full_cols_count * COMPLETE_COLUMNS_RATIO;
    let first_true_row_index = 0;
    for (let i = 0; i <= df.length; i++) {
      // TODO: Filter out datum entries that don't "count" as "real" content
      if (df[i].length >= COMPLETE_COLUMNS_THRESHOLD) {
        first_true_row_index = i;
        break;
      }
    }
    return [
      /*remaining:*/ df.slice(first_true_row_index, df.length),
      /*removed:*/ df.slice(0, first_true_row_index),
    ];
  }

  function getIndexColumns(dataframe) {
    let header_row = dataframe[0];
    let matched_raw_values = [];
    let matched_col_indices = [];
    let matched_standardized_values = [];
    header_row.forEach((element, index) => {
      if (Object.keys(ALL_INDEX_COLUMN_MAPPINGS).includes(element)) {
        matched_raw_values.push(element);
        matched_col_indices.push(index);
        matched_standardized_values.push(ALL_INDEX_COLUMN_MAPPINGS[element]);
      }
    });

    return [
      matched_raw_values,
      matched_col_indices,
      matched_standardized_values,
    ];
  }

  function trimTrailingRows(dataframe) {
    console.log("Here's what we're working with after headers:");
    console.log(dataframe);
    let last_true_row_index = dataframe.length - 1;
    //debugger;
    for (let i = dataframe.length - 1; i >= 0; i--) {
      // A valid ending row has nonnull values for all index columns
      // We can be even more expansive and say that all index columns need
      // to have JS "truthy" values to avoid issues of empty strings, etc.
      let detected_index_values = detected_index_columns[1].map(
        (x) => dataframe[i][x]
      );
      if (detected_index_values.every(Boolean)) {
        last_true_row_index = i;
        break;
      }
    }
    let output = [
      /*remaining:*/ dataframe.slice(0, last_true_row_index + 1),
      /*removed:*/ dataframe.slice(last_true_row_index + 1, dataframe.length),
    ];
    return output;
  }
</script>

<div class="sheet-trimmer-pane">
  <h3>Input data</h3>
  <div id="step-1-data" class="big-html-table">
    {@html parsed_original_HTML}
  </div>
  <button
    on:click={() => {
      [trimmed_array, trimmed_header_rows] = trimHeaderRows(active_sheet);
      //trimmed_header_row_count = trimmed_header_rows.length
      detected_index_columns = getIndexColumns(trimmed_array);
      [trimmed_array, trimmed_trailing_rows] = trimTrailingRows(trimmed_array);
    }}
  >
    Trim excess header and trailing rows from this table
  </button>
</div>
