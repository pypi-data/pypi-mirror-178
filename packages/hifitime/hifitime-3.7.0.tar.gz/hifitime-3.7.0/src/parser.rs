/*
 * Hifitime, part of the Nyx Space tools
 * Copyright (C) 2022 Christopher Rabotin <christopher.rabotin@gmail.com> et al. (cf. AUTHORS.md)
 * This Source Code Form is subject to the terms of the Apache
 * v. 2.0. If a copy of the Apache License was not distributed with this
 * file, You can obtain one at https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Documentation: https://nyxspace.com/
 */

use crate::{Errors, ParsingErrors};

#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub(crate) enum Token {
    Year,
    Month,
    Day,
    Hour,
    Minute,
    Second,
    Subsecond,
    OffsetHours,
    OffsetMinutes,
    Timescale,
}

impl Token {
    pub fn value_ok(&self, val: i32) -> Result<(), Errors> {
        match &self {
            Token::Year => Ok(()), // No validation on the year
            Token::Month => {
                if !(0..=13).contains(&val) {
                    Err(Errors::ParseError(ParsingErrors::ValueError))
                } else {
                    Ok(())
                }
            }
            Token::Day => {
                if !(0..=31).contains(&val) {
                    Err(Errors::ParseError(ParsingErrors::ValueError))
                } else {
                    Ok(())
                }
            }
            Token::Hour | Token::OffsetHours => {
                if !(0..=23).contains(&val) {
                    Err(Errors::ParseError(ParsingErrors::ValueError))
                } else {
                    Ok(())
                }
            }
            Token::Minute | Token::OffsetMinutes => {
                if !(0..=59).contains(&val) {
                    Err(Errors::ParseError(ParsingErrors::ValueError))
                } else {
                    Ok(())
                }
            }
            Token::Second => {
                if !(0..=60).contains(&val) {
                    Err(Errors::ParseError(ParsingErrors::ValueError))
                } else {
                    Ok(())
                }
            }
            Token::Subsecond => {
                if val < 0 {
                    Err(Errors::ParseError(ParsingErrors::ValueError))
                } else {
                    Ok(())
                }
            }
            Token::Timescale => Ok(()),
        }
    }

    /// Returns the position in the array for this token
    pub fn pos(&self) -> usize {
        match &self {
            Token::Year => 0,
            Token::Month => 1,
            Token::Day => 2,
            Token::Hour => 3,
            Token::Minute => 4,
            Token::Second => 5,
            Token::Subsecond => 6,
            Token::OffsetHours => 7,
            Token::OffsetMinutes => 8,
            Token::Timescale => unreachable!(),
        }
    }

    /// Updates the token to what it should be seeking next given the delimiting character
    /// and returns the position in the array where the parsed integer should live
    pub fn advance_with(&mut self, ending_char: char) -> Result<(), Errors> {
        match &self {
            Token::Year => {
                if ending_char == '-' {
                    *self = Token::Month;
                    Ok(())
                } else {
                    Err(Errors::ParseError(ParsingErrors::UnknownFormat))
                }
            }
            Token::Month => {
                if ending_char == '-' {
                    *self = Token::Day;
                    Ok(())
                } else {
                    Err(Errors::ParseError(ParsingErrors::UnknownFormat))
                }
            }
            Token::Day => {
                if ending_char == 'T' || ending_char == ' ' {
                    *self = Token::Hour;
                    Ok(())
                } else {
                    Err(Errors::ParseError(ParsingErrors::UnknownFormat))
                }
            }
            Token::Hour => {
                if ending_char == ':' {
                    *self = Token::Minute;
                    Ok(())
                } else {
                    Err(Errors::ParseError(ParsingErrors::UnknownFormat))
                }
            }
            Token::Minute => {
                if ending_char == ':' {
                    *self = Token::Second;
                    Ok(())
                } else {
                    Err(Errors::ParseError(ParsingErrors::UnknownFormat))
                }
            }
            Token::Second => {
                if ending_char == '.' {
                    *self = Token::Subsecond;
                } else if ending_char == ' ' || ending_char == 'Z' {
                    // There are no subseconds here, only room for a time scale
                    *self = Token::Timescale;
                } else if ending_char == '-' || ending_char == '+' {
                    // There are no subseconds here, but we're seeing the start of an offset
                    *self = Token::OffsetHours;
                } else {
                    return Err(Errors::ParseError(ParsingErrors::UnknownFormat));
                }
                Ok(())
            }
            Token::Subsecond => {
                if ending_char == ' ' || ending_char == 'Z' {
                    // There are no subseconds here, only room for a time scale
                    *self = Token::Timescale;
                } else if ending_char == '-' || ending_char == '+' {
                    // There are no subseconds here, but we're seeing the start of an offset
                    *self = Token::OffsetHours;
                } else {
                    return Err(Errors::ParseError(ParsingErrors::UnknownFormat));
                }
                Ok(())
            }
            Token::OffsetHours => {
                if ending_char == ':' {
                    *self = Token::OffsetMinutes;
                    Ok(())
                } else {
                    Err(Errors::ParseError(ParsingErrors::UnknownFormat))
                }
            }
            Token::OffsetMinutes => {
                if ending_char == ' ' || ending_char == 'Z' {
                    // Only room for a time scale
                    *self = Token::Timescale;
                    Ok(())
                } else {
                    Err(Errors::ParseError(ParsingErrors::UnknownFormat))
                }
            }
            Token::Timescale => Ok(()),
        }
    }
}
