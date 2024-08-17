# Basic Excel parse-and-clean application using Flask and Svelte

## Purpose

By design, this application uses an _extremely_ lightweight server setup. At the start, the server only does one thing: Serve up the client app contents as a single page with all the processing and feedback logic built in. This ensures that all data processing can happen directly on the user's machine/within their web browser, giving them control of the information and instantaneous feedback until they are ready to submit the result.

Therefore, this application setup should only be used when the scope of the data to be worked with is small, and the total business logic and formatting to power it emphasizes simplicity and efficiency. 

## Contents

## How to run

## How to modify
For changes related to the server, modifications can be made directly to the `server.py` Flask script.

For changes in the frontend client, modfiy the corresponding component or page file in the `client/src` subdirectory.

## How to contribute
Open an issue, and/or a pull request! I make no promises as to my availability as a one-person maintainer.

## Acknowledgements
Thanks to [this Medium post from Alex Cabrera](https://cabreraalex.medium.com/svelte-js-flask-combining-svelte-with-a-simple-backend-server-d1bc46190ab9) for guidance on how to set up the basic Svelte + Flask combo at the core of this implementation.