<script>
  import { utils } from "xlsx";
  import FileInput from './FileInput.svelte';
  import SheetTrimmer from './SheetTrimmer.svelte';
  let workbook;
  // TODO: Option for more than one active sheet
  $: active_sheet = workbook ? workbook.Sheets[workbook.SheetNames[0]] : null;
  let trimmed_array = [];
  //TODO: Remove this block -- possibly shift to stores?
  let trimmed_header_rows = [];
  let trimmed_trailing_rows = [];
  $: detected_index_columns = trimmed_array.length > 0 ? getIndexColumns(trimmed_array) : null;

  $: trimmed_header_rows_count = trimmed_header_rows.length;
  $: trimmed_trailing_rows_count = trimmed_trailing_rows.length;
  // End todo 

  let tall_array = [];
  
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

  const POST_PIVOT_LABELS_COLUMN_NAME = "column";
  const POST_PIVOT_VALUES_COLUMN_NAME = "value";

  const CUSTOM_INDEX_COLUMN_MAPPINGS = {
    "Layer 1": "index_level_1",
    "Layer 2": "index_level_2",
    "Layer 3": "index_level_3",
  };

  const ALL_INDEX_COLUMN_MAPPINGS = {
    ...DATE_COLUMN_MAPPINGS,
    ...CUSTOM_INDEX_COLUMN_MAPPINGS,
  };

  

  $: parsed_original_HTML = active_sheet
    ? utils.sheet_to_html(active_sheet)
    : null;

  $: trimmed_data_as_HTML_table = trimmed_array.length
    ? utils.sheet_to_html(utils.aoa_to_sheet(trimmed_array))
    : null;

  $: tall_data_as_HTML_table = tall_array.length
    ? utils.sheet_to_html(utils.aoa_to_sheet(tall_array))
    : null;



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

  function getNonIndexCoumns(dataframe) {
    let [index_column_labels, index_column_indices, _] =
      getIndexColumns(dataframe);
    let header_row = dataframe[0];
    // This monstrosity is apparently the best way to do a `range` operation in JavaScript
    let dataframe_column_indices = [...Array(header_row.length).keys()];

    let matched_col_indices = dataframe_column_indices.filter(
      (i) => !index_column_indices.includes(i)
    );
    let matched_raw_values = matched_col_indices.map((i) => header_row[i]);
    //let matched_standardized_values = [];
    return [matched_raw_values, matched_col_indices];
  }

  function get_fake_columns(dataframe) {
    // We define "fake" columns as a column that is either:
    // 1) Blank for all "real" rows (as defined above)
    // 2) Only has "fake" values, that are functionaly equivalent to blank
    var fake_values = ["-", "/", "NA", "N/A", "None", "."];
    // Important to note for point (2) does *not* apply to all zeroes --
    // That may be "real" 0s, or it could be "fake"; it can't be immediately
    // determined without context.
  }

  function pivot_to_tall(
    dataframe,
    new_index_column_label = "column",
    new_value_column_label = "value"
  ) {
    // It is not clear that JavaScript has a more efficient transformation means
    // readily available, so we use the basic loop version of iterating over all
    // input rows and appending them to an output data structure.
    // TODO: Consider whether index column information should be passed in, versus (re) derived here.
    // TODO: Consider whether to leverage an external library for the transformation, such as `tidy`
    //  https://github.com/pbeshai/tidy
    let [index_columns_labels, index_column_indices, _] =
      getIndexColumns(dataframe);
    let [value_columns_labels, value_column_indices] =
      getNonIndexCoumns(dataframe);

    // We have to populate the first row with the column labels we want in the final product...
    let output = [
      [...index_columns_labels, new_index_column_label, new_value_column_label],
    ];

    // ... but we also need to ignore the first row in the input data, since that header row information
    // will already have been extracted by the getIndexColumns and getNonIndexColumns function calls.
    for (let i = 1; i < dataframe.length; i++) {
      let row_contents = dataframe[i];
      let row_index_values = index_column_indices.map((x) => row_contents[x]);

      value_column_indices.forEach((element, index) => {
        output.push([
          ...row_index_values,
          value_columns_labels[index],
          row_contents[element],
        ]);
      });
    }
    return output;
  }
</script>

<svelte:head>
  <title>Excel Parser</title>
  <meta name="excel-parser" content="Transform Excel Files" />
</svelte:head>

<div class="text-column">
  <h1>Excel Parser</h1>

  <p>
    Upload an Excel file to this tab to see it quickly transformed into an HTML
    object.
  </p>

  <p>
    Then, step-by-step cleaning functions will help transform it to a clean,
    tall table, accounting for some common cases along the way.
  </p>
  <FileInput bind:workbook/>
  
  {#if parsed_original_HTML}
    <SheetTrimmer parsed_original_HTML = {parsed_original_HTML} bind:active_sheet bind:trimmed_array/>
  {/if}
  {#if trimmed_array.length}
    <h3>Trimmed data</h3>
    <p>
      {trimmed_header_rows_count} excess row(s) were removed the top of the sheet,
      and {trimmed_trailing_rows_count} row(s) were removed from the bottom. The
      trimmed table now looks like this:
    </p>
    <div id="step-2-data" class="big-html-table">
      {@html trimmed_data_as_HTML_table}
    </div>
    <p>
      The next step will pivot the table, such that there is only one row for
      each unique combination of index columns. (A.k.a, a "tall table.") From
      this data, the detected index columns are:
    </p>
    <ul>
      {#each detected_index_columns[0] as index_column_label}
        <li>{index_column_label}</li>
      {/each}
    </ul>
    <p>
      The rest of the columns in each row will be collapsed into two values,
      called:
    </p>
    <ul>
      <li>
        <b>{POST_PIVOT_LABELS_COLUMN_NAME}</b>, with the <i>name</i> from each other
        column.
      </li>
      <li>
        <b>{POST_PIVOT_VALUES_COLUMN_NAME}</b>, with the <i>value</i> in that column
        from the given row.
      </li>
    </ul>
    <button
      on:click={() => {
        tall_array = pivot_to_tall(
          trimmed_array,
          POST_PIVOT_LABELS_COLUMN_NAME,
          POST_PIVOT_VALUES_COLUMN_NAME
        );
        console.log("Behold, a tall table");
        console.log(tall_array);
      }}
    >
      Pivot this data using these indices
    </button>
    <!-- TODO: Add second button or option to manually override detected index columns. -->
  {/if}
  {#if tall_array.length}
    <h3>Pivoted tall data</h3>
    <p>Here is the reshaped data in the "tall" format.</p>
    <div id="step-3-data" class="big-html-table">
      {@html tall_data_as_HTML_table}
    </div>
    <p>
      And that's it! This data is now ready to be uploaded to the destination of
      your choosing.
    </p>
  {/if}
</div>

