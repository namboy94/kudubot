mod files;


/// Reads a file and returns the file's content as a String.
///
/// # Arguments
///
/// * `file_path` - The path to the file
///
/// # Return value
///
/// Returns the file's content
fn read_from_file(file_path: &str) -> String {

    let mut file: File = File::open(file_path).unwrap();
    let mut data: String = String::new();
    file.read_to_string(&mut data).unwrap();
    return data;

}