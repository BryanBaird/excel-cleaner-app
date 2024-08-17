# Client app (Svelte frontend)

## Contents
 - The `public` directory contains all assets that are accessible to the end user/client. This includes static html, universal style files, supporting images, etc.
   - The `public/build` sub-directory includes the compiled output JavaScript and other resources produced by Svelte.
   - `public/index.html` is the placeholder for the main index page. Changes made here _will_ show up in the ultimately served application, but it is much better to make changes within the Svelte framework under `src`.
 - The `src` directory includes the Svelte components that form the bulk of the client app design and functionality. **Look in this directory for the "meat" of the app to make changes.**
   - `src/main.js` is just the basic wrapper that calls the client app. It is best to not touch this unless much more complexity and compartamentalization logic is needed.
   - `src/App.svelte` is the primary application code assembled as a Svelte module -- HTML, JavaScript interactive components, and CSS styling.

## Making changes
Svelte is a complied language, with the output being "vanilla" JavaScript, HTML, and CSS. After making a modification to anything in the `src` directory, you will need to re-build by running the following commmand from the command line _within this directory_.
```npm run build```
(This assumes npm and Svelte are both installed. Details on that to come.)

## Key dependencies
 - The "xlsx" library here is the main pillar for initially parsing in the input Excel file to a JavaScript Array of Arrays that can then be manipulated using vanilla JavaScript logic. (Or, if needed in the future, some other JavaScript library/structure that is more suited to tabular data structures, a la Python's `pandas` or R's dataframes.)