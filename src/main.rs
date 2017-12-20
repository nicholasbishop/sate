extern crate pest;
#[macro_use] extern crate pest_derive;

use pest::{Parser, RuleType};
use pest::inputs::Input;
use pest::iterators::Pairs;

#[cfg(debug_assertions)]
const _GRAMMAR: &'static str = include_str!("sate.pest");

#[derive(Parser)]
#[grammar = "sate.pest"]
struct SateParser;

#[derive(Debug, PartialEq)]
struct Arg(String);

impl Arg {
    fn new<S: Into<String>>(value: S) -> Arg {
        Arg(value.into())
    }
}

#[derive(Debug, PartialEq)]
struct Call {
    name: String,
    args: Vec<Arg>,
}

impl Call {
    fn new<S: Into<String>>(name: S, args: Vec<Arg>) -> Call {
        Call { name: name.into(), args: args }
    }

    fn from_name<S: Into<String>>(name: S) -> Call {
        Call::new(name.into(), vec![])
    }
}

#[derive(Debug, PartialEq)]
enum Tag {
    Directive {
        calls: Vec<Call>,
    },
    Target {
        name: String,
        calls: Vec<Call>,
    },
}

impl Tag {
    fn directive(calls: Vec<Call>) -> Tag {
        Tag::Directive { calls: calls }
    }

    fn target<S: Into<String>>(name: S, calls: Vec<Call>) -> Tag {
        Tag::Target { name: name.into(), calls: calls }
    }

    fn target_from_name<S: Into<String>>(name: S) -> Tag {
        Tag::target(name, vec![])
    }

    fn parse_directive<R: RuleType, I: Input>(pairs: Pairs<R, I>) -> Option<Tag> {
        let calls = pairs.flatten().map(|pair| Call::from_name(pair.as_str())).collect();
        Some(Tag::directive(calls))
    }

    fn parse_target<R: RuleType, I: Input>(mut pairs: Pairs<R, I>) -> Option<Tag> {
        if let Some(pair) = pairs.next() {
            let name = pair.as_str();
            let calls = pairs.flatten().map(|pair| Call::from_name(pair.as_str())).collect();
            Some(Tag::target(name, calls))
        } else {
            None
        }
    }

    fn parse(text: &str) -> Option<Tag> {
        match SateParser::parse_str(Rule::tag, text) {
            Ok(mut pairs) => {
                pairs.next().and_then(|pair| {
                    match pair.as_rule() {
                        Rule::directive => {
                            Tag::parse_directive(pair.into_inner())
                        },
                        Rule::target => {
                            Tag::parse_target(pair.into_inner())
                        }
                        _ => unreachable!()
                    }
                })
            },
            Err(e) => {
                println!("{:#?}", e);
                None
            }
        }
    }
}


fn main() {
    let tag = Tag::parse(&"[a]");
    println!("tag: {:#?}", tag);
    //assert_eq!(Tag::parse(&"[a]").unwrap(), Tag::new(Some("a".to_string()), &vec!()));
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn simple_target() {
        assert_eq!(Tag::parse(&"[a]").unwrap(),
                   Tag::target_from_name("a"));
    }

    #[test]
    fn target_with_call() {
        assert_eq!(Tag::parse(&"[a b()]").unwrap(),
                   Tag::target("a", vec![Call::from_name("b")]));
    }

    #[test]
    fn target_with_call_and_args() {
        assert_eq!(Tag::parse(&"[a b(c)]").unwrap(),
                   Tag::target("a", vec![Call::new("b", vec![Arg::new("c")])]));
    }

    #[test]
    fn simple_directive() {
        assert_eq!(Tag::parse(&"[a()]").unwrap(),
                   Tag::directive(vec![Call::from_name("a")]));
    }
}
