include!(concat!(env!("OUT_DIR"), "/sate.rs"));

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ident() {
        assert_eq!(ident("abc").unwrap(), "abc");
        assert_eq!(ident("abc123").unwrap(), "abc123");
        assert!(ident("123").is_err());
    }

    #[test]
    fn test_arg_list() {
        assert_eq!(arg_list("a b c").unwrap(), vec!["a", "b", "c"]);
    }

    #[test]
    fn test_call() {
        assert_eq!(call("a()").unwrap(), Call::new("a", vec![]));
        assert_eq!(call("a(b cd)").unwrap(), Call::new("a", vec!["b", "cd"]));
    }

    #[test]
    fn test_tag_directive() {
        assert_eq!(tag_directive("[a()]").unwrap(),
                   Directive(vec![Call::new("a", vec![])]));
    }

    #[test]
    fn test_tag_target_simple() {
        assert_eq!(tag_target_header("[a]").unwrap(),
                   TargetHeader::new("a", vec![]));
    }

    #[test]
    fn test_tag_target_with_call() {
        assert_eq!(tag_target_header("[a b()]").unwrap(),
                   TargetHeader::new("a", vec![Call::new("b", vec![])]));
    }

    #[test]
    fn test_command() {
        assert_eq!(command("a\n").unwrap(), Command::new(None, "a"));
        assert!(command("[a]\n").is_err());
    }

    #[test]
    fn test_target() {
        assert_eq!(target("[a]\nfoo\n").unwrap(),
                   Target::new(
                       TargetHeader::new("a", vec![]),
                       vec![Command::new(None, "foo")]));
    }

    #[test]
    fn test_satefile() {
        let mut sfile = SateFile::new();
        sfile.add_target(Target::new(
            TargetHeader::new("a", vec![]),
            vec![Command::new(None, "b")]));
        sfile.add_target(Target::new(
            TargetHeader::new("c", vec![]),
            vec![Command::new(None, "d")]));
        assert_eq!(satefile("[a]\nb\n\n[c]\nd\n").unwrap(), sfile);
    }
}
