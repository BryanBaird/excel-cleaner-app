<script>
  import { read } from "xlsx";
  let files, fileInput;
  import {workbook} from './stores.js'
  //export let workbook;

  $: if (files) {
    console.log(`${files[0].name}`);
  }

  function parseExcelFile(my_file) {
    console.log("inside parse function with parameter my_file below:");
    console.log(my_file);
    var reader = new FileReader();
    reader.onload = (e) => {
      let data = e.target.result;
      workbook.set(read(data));
      console.log("workbook object read from data:");
      //console.log(workbook);
    };
    reader.readAsArrayBuffer(my_file);
  }
</script>

<div class="file-input-pane">
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
        //console.log(workbook);
      }}
    >
      Confirm and process
    </button>
  {/if}
</div>
