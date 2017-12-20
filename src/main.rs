// #[macro_use]
// extern crate nom;

// named!(ident<&str>, chain!(is_alphabetic >> is_alphanumeric));

#[derive(Debug, PartialEq)]
pub struct Call {
    name: String,
    args: Vec<String>,
}

impl Call {
    pub fn new<S: Into<String> + Clone>(name: S, args: Vec<S>) -> Call {
        Call {
            name: name.into(),
            args: args.iter().map(|a| (*a).clone().into()).collect()
        }
    }
}

#[derive(Debug, PartialEq)]
pub struct Directive(Vec<Call>);

#[derive(Debug, PartialEq)]
pub struct TargetHeader {
    name: String,
    calls: Vec<Call>,
}

#[derive(Debug, PartialEq)]
pub enum Tag {
    Directive(Directive),
    Target(TargetHeader),
}

impl Tag {
    fn directive(calls: Vec<Call>) -> Tag {
        Tag::Directive(Directive(calls))
    }

    fn target<S: Into<String>>(name: S, calls: Vec<Call>) -> Tag {
        Tag::Target(TargetHeader { name: name.into(), calls: calls })
    }
}

#[derive(Debug, PartialEq)]
pub struct Command {
    directive: Option<Directive>,
    code: String,
}

impl Command {
    fn new<S: Into<String>>(directive: Option<Directive>, code: S) -> Command {
        Command { directive, code: code.into() }
    }
}

#[derive(Debug, PartialEq)]
pub struct Target {
    header: TargetHeader,
    commands: Vec<Command>,
}

mod parse {
    include!(concat!(env!("OUT_DIR"), "/sate.rs"));
}

fn main() {
    
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ident() {
        assert_eq!(parse::ident("abc").unwrap(), "abc");
        assert_eq!(parse::ident("abc123").unwrap(), "abc123");
        assert!(parse::ident("123").is_err());
    }

    #[test]
    fn test_arg_list() {
        assert_eq!(parse::arg_list("a b c").unwrap(), vec!["a", "b", "c"]);
    }

    #[test]
    fn test_call() {
        assert_eq!(parse::call("a()").unwrap(), Call::new("a", vec![]));
        assert_eq!(parse::call("a(b cd)").unwrap(), Call::new("a", vec!["b", "cd"]));
    }

    #[test]
    fn test_tag_directive() {
        assert_eq!(parse::tag("[a()]").unwrap(),
                   Tag::directive(vec![Call::new("a", vec![])]));
    }

    #[test]
    fn test_tag_target_simple() {
        assert_eq!(parse::tag("[a]").unwrap(), Tag::target("a", vec![]));
    }

    #[test]
    fn test_tag_target_with_call() {
        assert_eq!(parse::tag("[a b()]").unwrap(), Tag::target("a", vec![Call::new("b", vec![])]));
    }

    #[test]
    fn test_command() {
        assert_eq!(parse::command("a\n").unwrap(), Command::new(None, "a"));
    }
}
