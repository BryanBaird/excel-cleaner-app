<script>
	import { read, utils } from "xlsx";
	let files, fileInput;
	let workbook;
	let trimmed_array = [];
	let trimmed_header_rows = [];
	let trimmed_trailing_rows = [];
	$: trimmed_header_rows_count = trimmed_header_rows.length;
	$: trimmed_trailing_rows_count = trimmed_trailing_rows.length;
  
	const COMPLETE_COLUMNS_RATIO = 0.9;
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
  
	let detected_index_columns = [];
  
	$: if (files) {
	  console.log(`${files[0].name}`);
	}
  
	$: active_sheet = workbook ? workbook.Sheets[workbook.SheetNames[0]] : null;
  
	$: parsed_original_HTML = active_sheet
	  ? utils.sheet_to_html(active_sheet)
	  : null;
  
	$: trimmed_data_as_HTML_table = trimmed_array.length
	  ? utils.sheet_to_html(utils.aoa_to_sheet(trimmed_array))
	  : null;
  
	function parseExcelFile(my_file) {
	  console.log("inside parse function with parameter my_file below:");
	  console.log(my_file);
	  var reader = new FileReader();
	  reader.onload = (e) => {
		let data = e.target.result;
		workbook = read(data);
		console.log("workbook object read from data:");
		console.log(workbook);
	  };
	  reader.readAsArrayBuffer(my_file);
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
	  let matched_col_indeces = [];
	  let matched_standardized_values = [];
	  header_row.forEach((element, index) => {
		if (Object.keys(ALL_INDEX_COLUMN_MAPPINGS).includes(element)) {
		  matched_raw_values.push(element);
		  matched_col_indeces.push(index);
		  matched_standardized_values.push(ALL_INDEX_COLUMN_MAPPINGS[element]);
		}
	  });
  
	  return [
		matched_raw_values,
		matched_col_indeces,
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
  
	function count_columns(dataframe) {
	  return dataframe.reduce(
		(maxLen, el, i, arr) => (el.length > maxLen ? el.length : maxLen),
		0
	  );
	}
  
	function get_fake_columns(dataframe) {
	  // We define "fake" columns as a column that is either:
	  // 1) Blank for all "real" rows (as defined above)
	  // 2) Only has "fake" values, that are functionaly equivalent to blank
	  var fake_values = ['-', '/', 'NA', 'N/A', 'None', '.']
	  // Important to note for point (2) does *not* apply to all zeroes --
	  // That may be "real" 0s, or it could be "fake"; it can't be immediately
	  // determined without context.
	  
  
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
  
	<label for="file_picker">Select an data file to process: </label>
	<input
	  bind:files
	  bind:this={fileInput}
	  type="file"
	  id="file_picker"
	  name="file_picker"
	  accept=".xls,.xlsx, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"
	/>
  
	{#if files}
	  <h3>Selected file:</h3>
	  {files[0].name}
	  <button
		on:click={() => {
		  console.log(`${files[0].name} will be processed`);
		  parseExcelFile(files[0]);
		  console.log(workbook);
		}}
	  >
		Confirm and process
	  </button>
	{/if}
	{#if parsed_original_HTML}
	  <h3>Input data</h3>
	  <div id="step-1-data" class="big-html-table">
		{@html parsed_original_HTML}
	  </div>
	  <button
		on:click={() => {
		  [trimmed_array, trimmed_header_rows] = trimHeaderRows(active_sheet);
		  //trimmed_header_row_count = trimmed_header_rows.length
		  detected_index_columns = getIndexColumns(trimmed_array);
		  [trimmed_array, trimmed_trailing_rows] =
			trimTrailingRows(trimmed_array);
		  debugger;
		}}
	  >
		Trim excess header and trailing rows from this table
	  </button>
	{/if}
	{#if trimmed_array.length}
	  {trimmed_header_rows_count} excess row(s) were removed the top of the sheet,
	  and {trimmed_trailing_rows_count} row(s) were removed from the bottom. The trimmed
	  table now looks like this:
	  <div id="step-2-data" class="big-html-table">
		{@html trimmed_data_as_HTML_table}
	  </div>
	{/if}
  </div>
  
  <style>
	div.big-html-table {
	  height: 230px;
	  width: 900px;
	  overflow: scroll;
	}
  </style>
  