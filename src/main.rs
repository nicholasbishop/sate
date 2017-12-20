#[macro_use]
extern crate nom;

named!(ident<&str>, chain!(is_alphabetic >> is_alphanumeric));

fn main() {
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn simple_ident() {
        assert_eq!(ident("a"), Done("", "a"));
    }
}
