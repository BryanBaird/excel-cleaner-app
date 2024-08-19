# Basic Excel parse-and-clean application using Flask and Svelte

## Purpose
Data scientists and data professionals love clean, orderly, well-formatted data. This may be "tidy" data, or it may be "tall" data for effiencit engineering or storage, or it may be some other format. But it usually emphasizes machine-readability and compatibility with code-based tools.

But in the real world, Excel spreadsheets are still a very common means of not only analyzing data, but also for data entry and collection, especially amongst non-data professionals.

This concept application is meant to provide an easy but customizable framework for use cases where the person submitting the data (as an Excel file) might not be the same as a data professional who is used to cleaning data with R, Python, or other similar tools. It is meant to quickly and efficiently transform the data directly within the submitter's browser, with low compute setup required, and no unnecessary steps being kicked off to a server that might process using some other technology. (Though in the future, this application will be set up to be extensible for different ways to `POST` and upload the data structure at the end.)

The application walks users step-by-step through basic data checks and transformations that have been done on their uploaded file, so that they can confirm it makes sense before uploading to whatever final destination is configured for the app's specific instance!

### Architecture caveat
By design, this application uses an _extremely_ lightweight server setup. At the start, the server only does one thing: Serve up the client app contents as a single page with all the processing and feedback logic built in. This ensures that all data processing can happen directly on the user's machine/within their web browser, giving them control of the information and instantaneous feedback until they are ready to submit the result.

Therefore, this application setup should only be used when the scope of the data to be worked with is small, and the total business logic and formatting to power it emphasizes simplicity and efficiency. 

## Contents

 - `server.py`: Primary home of the Flask backend server. Primarily just serves the main application as a page from `client`, though future updates may include `POST` command to upload the final standardized data to an outside location or database that expects the data in the cleaned up format.
 - `client/`: All front-end application code and supporting resources, both the Svelte source code and the compiled outputs that are served to the end user. See subdirectory for more details.
 - `testing_and_demo/`: Asset(s) to be used for either during development to stress test new scenarios, or to demonstrate operations. Includes a reference Excel file 

## How to run
While it is technically possible to run just the client component on its own using `npm`'s run capabilities, the preferred way is to launch the Flask server component. In this directory, excecute this command:
```python server.py```

## How to modify
For changes related to the server, modifications can be made directly to the `server.py` Flask script.

For changes in the frontend client, modfiy the corresponding component or page file in the `client/src` subdirectory. You will need to re-build/recompile the Svelte code for the changes to appear in the `public/build` directory to be served to the end user. To do so, navigate to the `client` directory and execute:
```npm run build```.
(Note that `npm` will need to be installed.)

## How to contribute
Open an issue, and/or a pull request! I make no promises as to my availability as a one-person maintainer.

## Acknowledgements
Thanks to [this Medium post from Alex Cabrera](https://cabreraalex.medium.com/svelte-js-flask-combining-svelte-with-a-simple-backend-server-d1bc46190ab9) for guidance on how to set up the basic Svelte + Flask combo at the core of this implementation.