import { writable } from 'svelte/store';

export const workbook = writable();
export const current_sheet = writable(0);
export const trimmed_array = writable(0);
export const detected_index_columns = writable(0);
export const trimmed_header_rows = writable(0);
export const trimmed_trailing_rows = writable(0);
