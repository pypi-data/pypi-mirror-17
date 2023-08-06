# -*- coding: utf-8 -*-

import unittest
from declarativeunittest import raises
import pytest

from construct import *
from construct.lib import *

from io import BytesIO
import os, random, itertools
import hashlib
ident = lambda x: x



class TestCore(unittest.TestCase):

    def test_byte(self):
        assert Byte.parse(b"\x00") == 0
        assert Byte.parse(b"\xff") == 255
        assert Byte.build(0) == b"\x00"
        assert Byte.build(255) == b"\xff"
        assert Byte.sizeof() == 1

    @pytest.mark.xfail(PY26, reason="struct.pack has silent overflow")
    def test_byte_overflow(self):
        assert raises(Byte.build, 300) == FieldError
        assert raises(Byte.build, 65536) == FieldError

    def test_ints(self):
        assert Int8ub.parse(b"\x01") == 0x01
        assert Int8ub.build(0x01) == b"\x01"
        assert Int8ub.sizeof() == 1
        assert Int16ub.parse(b"\x01\x02") == 0x0102
        assert Int16ub.build(0x0102) == b"\x01\x02"
        assert Int16ub.sizeof() == 2
        assert Int32ub.parse(b"\x01\x02\x03\x04") == 0x01020304
        assert Int32ub.build(0x01020304) == b"\x01\x02\x03\x04"
        assert Int32ub.sizeof() == 4
        assert Int64ub.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08") == 0x0102030405060708
        assert Int64ub.build(0x0102030405060708) == b"\x01\x02\x03\x04\x05\x06\x07\x08"
        assert Int64ub.sizeof() == 8
        assert Int8sb.parse(b"\x01") == 0x01
        assert Int8sb.build(0x01) == b"\x01"
        assert Int8sb.sizeof() == 1
        assert Int16sb.parse(b"\x01\x02") == 0x0102
        assert Int16sb.build(0x0102) == b"\x01\x02"
        assert Int16sb.sizeof() == 2
        assert Int32sb.parse(b"\x01\x02\x03\x04") == 0x01020304
        assert Int32sb.build(0x01020304) == b"\x01\x02\x03\x04"
        assert Int32sb.sizeof() == 4
        assert Int64sb.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08") == 0x0102030405060708
        assert Int64sb.build(0x0102030405060708) == b"\x01\x02\x03\x04\x05\x06\x07\x08"
        assert Int64sb.sizeof() == 8
        assert Int8ul.parse(b"\x01") == 0x01
        assert Int8ul.build(0x01) == b"\x01"
        assert Int8ul.sizeof() == 1
        assert Int16ul.parse(b"\x01\x02") == 0x0201
        assert Int16ul.build(0x0201) == b"\x01\x02"
        assert Int16ul.sizeof() == 2
        assert Int32ul.parse(b"\x01\x02\x03\x04") == 0x04030201
        assert Int32ul.build(0x04030201) == b"\x01\x02\x03\x04"
        assert Int32ul.sizeof() == 4
        assert Int64ul.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08") == 0x0807060504030201
        assert Int64ul.build(0x0807060504030201) == b"\x01\x02\x03\x04\x05\x06\x07\x08"
        assert Int64ul.sizeof() == 8
        assert Int8sl.parse(b"\x01") == 0x01
        assert Int8sl.build(0x01) == b"\x01"
        assert Int8sl.sizeof() == 1
        assert Int16sl.parse(b"\x01\x02") == 0x0201
        assert Int16sl.build(0x0201) == b"\x01\x02"
        assert Int16sl.sizeof() == 2
        assert Int32sl.parse(b"\x01\x02\x03\x04") == 0x04030201
        assert Int32sl.build(0x04030201) == b"\x01\x02\x03\x04"
        assert Int32sl.sizeof() == 4
        assert Int64sl.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08") == 0x0807060504030201
        assert Int64sl.build(0x0807060504030201) == b"\x01\x02\x03\x04\x05\x06\x07\x08"
        assert Int64sl.sizeof() == 8

    def test_ints24(self):
        assert Int24ub.parse(b"\x01\x02\x03") == 0x010203
        assert Int24ub.build(0x010203) == b"\x01\x02\x03"
        assert Int24ub.sizeof() == 3
        assert Struct('int24' / Int24ub).parse(b"\x01\x02\x03") == Container(int24=0x010203)
        assert Struct('int24' / Int24ub).build(Container(int24=0x010203)) == b"\x01\x02\x03"
        assert Struct('int24' / Int24ub).sizeof() == 3

        assert Int24ul.parse(b"\x01\x02\x03") == 0x030201
        assert Int24ul.build(0x030201) == b"\x01\x02\x03"
        assert Int24ul.sizeof() == 3
        assert Struct('int24' / Int24ul).parse(b"\x01\x02\x03") == Container(int24=0x030201)
        assert Struct('int24' / Int24ul).build(Container(int24=0x030201)) == b"\x01\x02\x03"
        assert Struct('int24' / Int24ul).sizeof() == 3

    def test_varint(self):
        for n in [0,1,5,100,255,256,65535,65536,2**32,2**100]:
            assert VarInt.parse(VarInt.build(n)) == n
            assert len(VarInt.build(n)) >= len("%x" % n)//2
        for n in range(0, 127):
            assert VarInt.build(n) == int2byte(n)

        assert raises(VarInt.parse, b"") == FieldError
        assert raises(VarInt.build, -1) == ValueError
        assert raises(VarInt.sizeof) == SizeofError

    def test_varint_randomized(self):
        for i in range(100):
            x = random.randrange(0, 2**1024)
            assert VarInt.parse(VarInt.build(x)) == x
            b = os.urandom(1024) + b"\x00\xff"
            b = VarInt.build(VarInt.parse(b))
            assert b.startswith(VarInt.build(VarInt.parse(b)))

    def test_floats(self):
        assert Single.build(1.2) == b"?\x99\x99\x9a"
        assert Double.build(1.2) == b"?\xf3333333"

    def test_floats_randomized(self):
        for i in range(100):
            x = random.random()
            assert abs(Single.parse(Single.build(x)) - x) < 1e-3
            assert Double.parse(Double.build(x)) == x

    def test_bytes(self):
        assert Bytes(4).parse(b"12345678") == b"1234"
        assert Bytes(4).build(b"1234") == b"1234"
        assert raises(Bytes(4).parse, b"") == FieldError
        assert raises(Bytes(4).build, b"toolong") == FieldError
        assert Bytes(4).build(1) == b"\x00\x00\x00\x01"
        assert Bytes(4).build(0x01020304) == b"\x01\x02\x03\x04"
        assert Bytes(4).sizeof() == 4

        assert Bytes(lambda ctx: ctx.n).parse(b"12345678",n=4) == b"1234"
        assert Bytes(lambda ctx: ctx.n).build(b"1234",n=4) == b"1234"
        assert Bytes(lambda ctx: ctx.n).sizeof(n=4) == 4
        assert Bytes(lambda ctx: ctx.n).build(1, n=4) == b"\x00\x00\x00\x01"
        assert raises(Bytes(lambda ctx: ctx.n).build, b"", n=4) == FieldError
        assert raises(Bytes(lambda ctx: ctx.n).build, b"toolong", n=4) == FieldError
        assert raises(Bytes(lambda ctx: ctx.n).sizeof) == AttributeError

    def test_greedybytes(self):
        assert GreedyBytes.parse(b"1234") == b"1234"
        assert GreedyBytes.build(b"1234") == b"1234"
        assert raises(GreedyBytes.sizeof) == SizeofError

    def test_formatfield(self):
        assert FormatField("<","L").parse(b"\x12\x34\x56\x78") == 0x78563412
        assert FormatField("<","L").build(0x78563412) == b"\x12\x34\x56\x78"
        assert raises(FormatField("<","L").parse, b"") == FieldError
        assert raises(FormatField("<","L").parse, b"\x12\x34\x56") == FieldError
        assert raises(FormatField("<","L").build, "string not int") == FieldError
        assert FormatField("<","L").sizeof() == 4

    def test_formatfield_ints_randomized(self):
        for endianess,dtype in itertools.product("<>=","bhlqBHLQ"):
            d = FormatField(endianess, dtype)
            for i in range(100):
                x = random.randrange(0, 256**d.sizeof()//2)
                assert d.parse(d.build(x)) == x
            for i in range(100):
                b = os.urandom(d.sizeof())
                assert d.build(d.parse(b)) == b

    @pytest.mark.xfail(reason="float unpack on random bytes fails randomly")
    def test_formatfield_floats_randomized(self):
        # there is a roundoff eror because Python float is a C double
        # http://stackoverflow.com/questions/39619636/struct-unpackstruct-packfloat-has-roundoff-error
        for endianess,dtype in itertools.product("<>=","fd"):
            d = FormatField(endianess, dtype)
            for i in range(100):
                x = random.random()*12345
                if dtype == "d":
                    assert d.parse(d.build(x)) == x
                else:
                    assert abs(d.parse(d.build(x)) - x) < 1e-3
            for i in range(100):
                # this fails
                b = os.urandom(d.sizeof())
                assert d.build(d.parse(b)) == b

    @pytest.mark.xfail(PY26, reason="struct.pack has silent overflow")
    def test_formatfield_overflow(self):
        assert raises(FormatField("<","L").build, 2**100) == FieldError
        assert raises(FormatField("<","L").build, 9e9999) == FieldError

    def test_array(self):
        assert Byte[4].parse(b"1234") == [49, 50, 51, 52]
        assert Byte[4].build([49, 50, 51, 52]) == b"1234"

        assert Array(3,Byte).parse(b"\x01\x02\x03") == [1,2,3]
        assert Array(3,Byte).build([1,2,3]) == b"\x01\x02\x03"
        assert Array(3,Byte).parse(b"\x01\x02\x03additionalgarbage") == [1,2,3]
        assert raises(Array(3,Byte).parse, b"") == ArrayError
        assert raises(Array(3,Byte).build, [1,2]) == ArrayError
        assert raises(Array(3,Byte).build, [1,2,3,4,5,6,7,8]) == ArrayError
        assert Array(3,Byte).sizeof() == 3

        assert Array(lambda ctx: 3, Byte).parse(b"\x01\x02\x03", n=3) == [1,2,3]
        assert Array(lambda ctx: 3, Byte).parse(b"\x01\x02\x03additionalgarbage", n=3) == [1,2,3]
        assert raises(Array(lambda ctx: 3, Byte).parse, b"", n=3) == ArrayError
        assert Array(lambda ctx: 3, Byte).build([1,2,3], n=3) == b"\x01\x02\x03"
        assert raises(Array(lambda ctx: 3, Byte).build, [1,2], n=3) == ArrayError
        assert Array(lambda ctx: ctx.n, Byte).parse(b"\x01\x02\x03", n=3) == [1,2,3]
        assert Array(lambda ctx: ctx.n, Byte).build([1,2,3], n=3) == b"\x01\x02\x03"
        assert raises(Array(lambda ctx: ctx.n, Byte).sizeof) == AttributeError
        assert Array(lambda ctx: ctx.n, Byte).sizeof(n=4) == 4

    def test_prefixedarray(self):
        assert PrefixedArray(Byte,Byte).parse(b"\x02\x0a\x0b") == [10,11]
        assert PrefixedArray(Byte,Byte).build([10,11]) == b"\x02\x0a\x0b"
        assert raises(PrefixedArray(Byte,Byte).sizeof) == SizeofError

    def test_range(self):
        assert Byte[2:4].parse(b"1234567890") == [49, 50, 51, 52]
        assert Byte[2:4].build([49, 50, 51, 52]) == b"1234"
        assert Byte[:4].parse(b"1234567890") == [49, 50, 51, 52]
        assert Byte[:4].build([49, 50, 51, 52]) == b"1234"
        assert raises(Byte[2:].parse, b"") == RangeError
        assert raises(Byte[2:].build, []) == RangeError

        assert Range(3, 5, Byte).parse(b"\x01\x02\x03") == [1,2,3]
        assert Range(3, 5, Byte).parse(b"\x01\x02\x03\x04") == [1,2,3,4]
        assert Range(3, 5, Byte).parse(b"\x01\x02\x03\x04\x05") == [1,2,3,4,5]
        assert Range(3, 5, Byte).parse(b"\x01\x02\x03\x04\x05\x06") == [1,2,3,4,5]
        assert raises(Range(3, 5, Byte).parse, b"") == RangeError
        assert Range(3, 5, Byte).build([1,2,3]) == b"\x01\x02\x03"
        assert Range(3, 5, Byte).build([1,2,3,4]) == b"\x01\x02\x03\x04"
        assert Range(3, 5, Byte).build([1,2,3,4,5]) == b"\x01\x02\x03\x04\x05"
        assert raises(Range(3, 5, Byte).build, [1,2]) == RangeError
        assert raises(Range(3, 5, Byte).build, [1,2,3,4,5,6]) == RangeError
        assert raises(Range(3, 5, Byte).build, 0) == RangeError
        assert raises(Range(3, 5, Byte).sizeof) == SizeofError
        assert Range(0, 100, Struct("id"/Byte)).parse(b'\x01\x02') == [Container(id=1),Container(id=2)]
        assert Range(0, 100, Struct("id"/Byte)).build([dict(id=i) for i in range(5)]) == b'\x00\x01\x02\x03\x04'
        assert raises(Range(0, 100, Struct("id"/Byte)).build, dict(id=1)) == RangeError
        assert raises(Range(0, 100, Struct("id"/Byte)).sizeof) == SizeofError
        assert raises(Range, -2, +7, Byte) == RangeError
        assert raises(Range, -2, -7, Byte) == RangeError
        assert raises(Range, +2, -7, Byte) == RangeError
        assert Range(1, 1, Byte).sizeof() == 1
        assert raises(Range(1, 1, VarInt).sizeof) == SizeofError

    def test_greedyrange(self):
        assert GreedyRange(Byte).parse(b"") == []
        assert GreedyRange(Byte).build([]) == b""
        assert GreedyRange(Byte).parse(b"\x01\x02") == [1,2]
        assert GreedyRange(Byte).build([1,2]) == b"\x01\x02"
        assert raises(GreedyRange(Byte).sizeof) == SizeofError

    def test_repeatuntil(self):
        assert RepeatUntil(lambda obj,ctx: obj == 9, Byte).parse(b"\x02\x03\x09garbage") == [2,3,9]
        assert RepeatUntil(lambda obj,ctx: obj == 9, Byte).build([2,3,9,1,1,1]) == b"\x02\x03\x09"
        assert raises(RepeatUntil(lambda obj,ctx: obj == 9, Byte).parse, b"\x02\x03\x08") == ArrayError
        assert raises(RepeatUntil(lambda obj,ctx: obj == 9, Byte).build, [2,3,8]) == ArrayError
        assert raises(RepeatUntil(lambda obj,ctx: obj == 9, Byte).sizeof) == SizeofError

    def test_struct(self):
        assert Struct("a" / Int16ul, "b" / Byte).parse(b"\x01\x00\x02") == Container(a=1)(b=2)
        assert Struct("a" / Int16ul, "b" / Byte).build(Container(a=1)(b=2)) == b"\x01\x00\x02"
        assert Struct("a"/Struct("b"/Byte)).parse(b"\x01") == Container(a=Container(b=1))
        assert Struct("a"/Struct("b"/Byte)).build(Container(a=Container(b=1))) == b"\x01"
        assert Struct("a"/Struct("b"/Byte)).sizeof() == 1
        assert raises(Struct("missingkey"/Byte).build, dict()) == KeyError
        assert Struct("a"/Byte, "a"/VarInt, "a"/Pass).build(dict(a=1)) == b"\x01\x01"
        assert Struct().parse(b"") == Container()
        assert Struct().build(dict()) == b""
        assert Struct(Padding(2)).parse(b"\x00\x00") == Container()
        assert Struct(Padding(2)).build(dict()) == b"\x00\x00"
        assert Struct(Padding(2)).sizeof() == 2

    def test_struct_nested_embedded(self):
        assert Struct("a" / Byte, "b" / Int16ub, "inner" / Struct("c" / Byte, "d" / Byte)).parse(b"\x01\x00\x02\x03\x04") == Container(a=1)(b=2)(inner=Container(c=3)(d=4))
        assert Struct("a" / Byte, "b" / Int16ub, "inner" / Struct("c" / Byte, "d" / Byte)).build(Container(a=1)(b=2)(inner=Container(c=3)(d=4))) == b"\x01\x00\x02\x03\x04"
        assert Struct("a" / Byte, "b" / Int16ub, Embedded("inner" / Struct("c" / Byte, "d" / Byte))).parse(b"\x01\x00\x02\x03\x04") == Container(a=1)(b=2)(c=3)(d=4)
        assert Struct("a" / Byte, "b" / Int16ub, Embedded("inner" / Struct("c" / Byte, "d" / Byte))).build(Container(a=1)(b=2)(c=3)(d=4)) == b"\x01\x00\x02\x03\x04"

    def test_sequence(self):
        assert Sequence(Int8ub, Int16ub).parse(b"\x01\x00\x02") == [1,2]
        assert Sequence(Int8ub, Int16ub).build([1,2]) == b"\x01\x00\x02"

    def test_sequence_nested_embedded(self):
        assert Sequence(Int8ub, Int16ub, Sequence(Int8ub, Int8ub)).parse(b"\x01\x00\x02\x03\x04") == [1,2,[3,4]]
        assert Sequence(Int8ub, Int16ub, Sequence(Int8ub, Int8ub)).build([1,2,[3,4]]) == b"\x01\x00\x02\x03\x04"
        assert Sequence(Int8ub, Int16ub, Embedded(Sequence(Int8ub, Int8ub))).parse(b"\x01\x00\x02\x03\x04") == [1,2,3,4]
        assert Sequence(Int8ub, Int16ub, Embedded(Sequence(Int8ub, Int8ub))).build([1,2,3,4]) == b"\x01\x00\x02\x03\x04"

    def test_computed(self):
        assert Computed(lambda ctx: "moo").parse(b"") == "moo"
        assert Computed(lambda ctx: "moo").build(None) == b""
        assert Computed(lambda ctx: "moo").sizeof() == 0
        assert Struct("c" / Computed(lambda ctx: "moo")).parse(b"") == Container(c="moo")
        assert Struct("c" / Computed(lambda ctx: "moo")).build({}) == b""
        assert Struct("c" / Computed(lambda ctx: "moo")).build(dict()) == b""
        assert Struct("c" / Computed(lambda ctx: "moo")).build(Container()) == b""
        assert raises(Computed(lambda ctx: ctx.missing).parse, b"") == AttributeError
        assert raises(Computed(lambda ctx: ctx["missing"]).parse, b"") == KeyError

    def test_rawcopy(self):
        assert RawCopy(Byte).parse(b"\xff") == dict(data=b"\xff", value=255, offset1=0, offset2=1, length=1)
        assert RawCopy(Byte).build(dict(data=b"\xff")) == b"\xff"
        assert RawCopy(Byte).build(dict(value=255)) == b"\xff"
        assert RawCopy(Byte).sizeof() == 1

    def test_tell(self):
        assert Tell.parse(b"") == 0
        assert Tell.build(None) == b""
        assert Tell.sizeof() == 0
        assert Struct("a"/Tell, "b"/Byte, "c"/Tell).parse(b"\xff") == Container(a=0)(b=255)(c=1)
        assert Struct("a"/Tell, "b"/Byte, "c"/Tell).build(Container(a=0)(b=255)(c=1)) == b"\xff"
        assert Struct("a"/Tell, "b"/Byte, "c"/Tell).build(dict(b=255)) == b"\xff"

    def test_seek(self):
        assert (Seek(5) >> Byte).parse(b"01234x") == [5,120]
        assert (Bytes(10) >> Seek(5) >> Byte).build([b"0123456789",None,255]) == b"01234\xff6789"
        assert Seek(5).parse(b"") == 5
        assert Seek(5).build(None) == b""
        assert raises(Seek(5).sizeof) == SizeofError

    def test_pass(self):
        assert Pass.parse(b"") == None
        assert Pass.build(None) == b""
        assert Pass.sizeof() == 0
        assert Struct("pass"/Pass).build(dict()) == b""

    def test_terminator(self):
        assert Terminator.parse(b"") == None
        assert raises(Terminator.parse, b"x") == TerminatorError
        assert Terminator.build(None) == b""
        assert Terminator.sizeof() == 0
        assert Struct("end"/Terminator).build(dict()) == b""
        assert Struct(Terminator).build(dict()) == b""

    def test_pointer(self):
        assert Pointer(lambda ctx: 2, "pointer" / Int8ub).parse(b"\x00\x00\x07") == 7
        assert Pointer(lambda ctx: 2, "pointer" / Int8ub).build(7) == b"\x00\x00\x07"
        assert Pointer(lambda ctx: 2, "pointer" / Int8ub).sizeof() == 0

    def test_const(self):
        assert Const(b"MZ").parse(b"MZ") == b"MZ"
        assert Const(b"MZ").build(None) == b"MZ"
        assert Const(b"MZ").build(b"MZ") == b"MZ"
        assert Const(b"MZ").sizeof() == 2
        assert Const(Bytes(4), b"****").parse(b"****") == b"****"
        assert Const(Bytes(4), b"****").build(None) == b"****"
        assert Const(Bytes(4), b"****").build(b"****") == b"****"
        assert Const(Bytes(4), b"****").sizeof() == 4
        assert Const(Int32ul, 255).parse(b"\xff\x00\x00\x00") == 255
        assert Const(Int32ul, 255).build(None) == b"\xff\x00\x00\x00"
        assert Const(Int32ul, 255).build(255) == b"\xff\x00\x00\x00"
        assert Const(Int32ul, 255).sizeof() == 4
        assert raises(Const(b"MZ").parse, b"ELF") == ConstError
        assert raises(Const(b"MZ").build, b"???") == ConstError
        assert raises(Const(Int32ul, 255).parse, b"\x00\x00\x00\x00") == ConstError
        assert Struct("sig" / Const(b"MZ")).parse(b"MZ") == Container(sig=b"MZ")
        assert Struct("sig" / Const(b"MZ")).build(Container(sig=b"MZ")) == b"MZ"
        assert Struct("sig" / Const(b"MZ")).build(Container()) == b"MZ"
        assert Struct("sig" / Const(b"MZ")).sizeof() == 2

    def test_switch(self):
        assert Switch(lambda ctx: 5, {1:Byte, 5:Int16ub}).parse(b"\x00\x02") == 2
        assert Switch(lambda ctx: 6, {1:Byte, 5:Int16ub}, default=Byte).parse(b"\x00\x02") == 0
        assert Switch(lambda ctx: 5, {1:Byte, 5:Int16ub}, includekey=True).parse(b"\x00\x02") == (5,2)
        assert Switch(lambda ctx: 5, {1:Byte, 5:Int16ub}).build(2) == b"\x00\x02"
        assert Switch(lambda ctx: 6, {1:Byte, 5:Int16ub}, default=Byte).build(9) == b"\x09"
        assert Switch(lambda ctx: 5, {1:Byte, 5:Int16ub}, includekey=True).build((5,2)) == b"\x00\x02"
        assert raises(Switch(lambda ctx: 6, {1:Byte, 5:Int16ub}).parse, b"\x00\x02") == SwitchError
        assert raises(Switch(lambda ctx: 6, {1:Byte, 5:Int16ub}).build, 9) == SwitchError
        assert raises(Switch(lambda ctx: 5, {1:Byte, 5:Int16ub}, includekey=True).build, (89,2)) == SwitchError
        assert raises(Switch(lambda ctx: 5, {1:Byte, 5:Int16ub}).sizeof) == SizeofError

    def test_ifthenelse(self):
        assert IfThenElse(lambda ctx: True,  Int8ub, Int16ub).parse(b"\x01") == 1
        assert IfThenElse(lambda ctx: False, Int8ub, Int16ub).parse(b"\x00\x01") == 1
        assert IfThenElse(lambda ctx: True,  Int8ub, Int16ub).build(1) == b"\x01"
        assert IfThenElse(lambda ctx: False, Int8ub, Int16ub).build(1) == b"\x00\x01"
        assert raises(IfThenElse(lambda ctx: False, Int8ub, Int16ub).sizeof) == SizeofError

    def test_if(self):
        assert If(lambda ctx: True,  Int8ub).parse(b"\x01") == 1
        assert If(lambda ctx: False, Int8ub).parse(b"") == None
        assert If(lambda ctx: True,  Int8ub).build(1) == b"\x01"
        assert If(lambda ctx: False, Int8ub).build(None) == b""
        assert raises(If(lambda ctx: False, Int8ub).sizeof) == SizeofError

    def test_padding(self):
        assert Padding(4).parse(b"\x00\x00\x00\x00") == None
        assert Padding(4).build(None) == b"\x00\x00\x00\x00"
        assert Padding(4).sizeof() == 4
        assert Padding(4, strict=True).parse(b"\x00\x00\x00\x00") == None
        assert Padding(4, strict=True).build(None) == b"\x00\x00\x00\x00"
        assert Padding(4, pattern=b'x', strict=True).parse(b"xxxx") == None
        assert raises(Padding(4, strict=True).parse, b"????") == PaddingError
        assert raises(Padding(4, pattern=b'x', strict=True).parse, b"????") == PaddingError
        assert raises(Padding, 4, pattern=b"??") == PaddingError
        assert raises(Padding, 4, pattern=u"?") == PaddingError

    def test_padded(self):
        assert Padded(4, Byte).parse(b"\x01\x00\x00\x00") == 1
        assert Padded(4, Byte).build(1) == b"\x01\x00\x00\x00"
        assert Padded(4, Byte).sizeof() == 4
        assert Padded(4, Byte, strict=True).parse(b"\x01\x00\x00\x00") == 1
        assert raises(Padded(4, Byte, strict=True).parse, b"\x01???") == PaddingError
        assert Padded(4, Byte, strict=True).build(1) == b"\x01\x00\x00\x00"
        assert Padded(4, Byte, pattern=b'x', strict=True).parse(b"\x01xxx") == 1
        assert raises(Padded(4, Byte, pattern=b'x', strict=True).parse, b"\x01???") == PaddingError
        assert raises(Padded, 4, Byte, pattern=b"??") == PaddingError
        assert raises(Padded, 4, Byte, pattern=u"?") == PaddingError

    def test_aligned(self):
        assert Aligned(Byte, modulus=4).parse(b"\x01\x00\x00\x00") == 1
        assert Aligned(Byte, modulus=4).build(1) == b"\x01\x00\x00\x00"
        assert Aligned(Byte, modulus=4).sizeof() == 4
        assert Struct(Aligned("a"/Byte, modulus=4), "b"/Byte).parse(b"\x01\x00\x00\x00\x02") == Container(a=1)(b=2)
        assert Struct(Aligned("a"/Byte, modulus=4), "b"/Byte).build(Container(a=1)(b=2)) == b"\x01\x00\x00\x00\x02"
        assert Struct(Aligned("a"/Byte, modulus=4), "b"/Byte).sizeof() == 5
        assert Aligned(Int8ub,  modulus=4).build(1) == b"\x01\x00\x00\x00"
        assert Aligned(Int16ub, modulus=4).build(1) == b"\x00\x01\x00\x00"
        assert Aligned(Int32ub, modulus=4).build(1) == b"\x00\x00\x00\x01"
        assert Aligned(Int64ub, modulus=4).build(1) == b"\x00\x00\x00\x00\x00\x00\x00\x01"
        assert Aligned(Byte, modulus=this.m).parse(b"\xff\x00", dict(m=2)) == 255
        assert Aligned(Byte, modulus=this.m).build(255, dict(m=2)) == b"\xff\x00"
        assert Aligned(Byte, modulus=this.m).sizeof(dict(m=2)) == 2

    def test_alignedstruct(self):
        assert AlignedStruct("a"/Int8ub, "b"/Int16ub, modulus=4, pattern=b"?").parse(b"\x01???\x00\x05??") == Container(a=1)(b=5)
        assert AlignedStruct("a"/Int8ub, "b"/Int16ub, modulus=4, pattern=b"?").build(dict(a=1,b=5)) == b"\x01???\x00\x05??"

    def test_from_issue_87(self):
        assert ("string_name" / Byte).parse(b"\x01") == 1
        assert (u"unicode_name" / Byte).parse(b"\x01") == 1
        assert (b"bytes_name" / Byte).parse(b"\x01") == 1
        assert (None / Byte).parse(b"\x01") == 1

    def test_operators(self):
        assert Struct("new" / ("old" / Byte)).parse(b"\x01") == Container(new=1)
        assert Struct("new" / ("old" / Byte)).build(Container(new=1)) == b"\x01"
        assert Byte[4].parse(b"\x01\x02\x03\x04") == [1,2,3,4]
        assert Byte[4].build([1,2,3,4]) == b"\x01\x02\x03\x04"
        assert raises(Byte[2:3].parse, b"\x01") == RangeError
        assert Byte[2:3].parse(b"\x01\x02") == [1,2]
        assert Byte[2:3].parse(b"\x01\x02\x03") == [1,2,3]
        assert Byte[2:3].parse(b"\x01\x02\x03") == [1,2,3]
        assert Byte[2:3].parse(b"\x01\x02\x03\x04") == [1,2,3]
        assert Struct("nums" / Byte[4]).parse(b"\x01\x02\x03\x04") == Container(nums=[1,2,3,4])
        assert Struct("nums" / Byte[4]).build(Container(nums=[1,2,3,4])) == b"\x01\x02\x03\x04"
        assert (Int8ub >> Int16ub).parse(b"\x01\x00\x02") == [1,2]
        assert (Int8ub >> Int16ub >> Int32ub).parse(b"\x01\x00\x02\x00\x00\x00\x03") == [1,2,3]
        assert (Int8ub[2] >> Int16ub[2]).parse(b"\x01\x02\x00\x03\x00\x04") == [[1,2],[3,4]]

    def test_renamed(self):
        assert Struct(Renamed("new", Renamed("old", Byte))).parse(b"\x01") == Container(new=1)
        assert Struct(Renamed("new", Renamed("old", Byte))).build(Container(new=1)) == b"\x01"

    def test_alias(self):
        assert Alias("b","a").parse(b"",Container(a=1)) == 1
        assert Alias("b","a").build(None,Container(a=1)) == b""
        assert Alias("b","a").sizeof() == 0
        assert Struct("a"/Byte, Alias("b","a")).parse(b"\x01") == Container(a=1)(b=1)
        assert Struct("a"/Byte, Alias("b","a")).build(dict(a=1)) == b"\x01"
        assert Struct("a"/Byte, Alias("b","a")).sizeof() == 1

    def test_bitsinteger(self):
        assert BitsInteger(8).parse(b"\x01\x01\x01\x01\x01\x01\x01\x01") == 255
        assert BitsInteger(8).build(255) == b"\x01\x01\x01\x01\x01\x01\x01\x01"
        assert BitsInteger(8).sizeof() == 8
        assert BitsInteger(8, signed=True).parse(b"\x01\x01\x01\x01\x01\x01\x01\x01") == -1
        assert BitsInteger(8, signed=True).build(-1) == b"\x01\x01\x01\x01\x01\x01\x01\x01"
        assert BitsInteger(8, swapped=True, bytesize=4).parse(b"\x01\x01\x01\x01\x00\x00\x00\x00") == 0x0f
        assert BitsInteger(8, swapped=True, bytesize=4).build(0x0f) == b"\x01\x01\x01\x01\x00\x00\x00\x00"
        assert BitsInteger(lambda ctx: 8).parse(b"\x01" * 8) == 255
        assert BitsInteger(lambda ctx: 8).build(255) == b"\x01" * 8
        assert BitsInteger(lambda ctx: 8).sizeof() == 8

    def test_bytesinteger(self):
        assert BytesInteger(4).parse(b"\x00\x00\x00\xff") == 255
        assert BytesInteger(4).build(255) == b"\x00\x00\x00\xff"
        assert BytesInteger(4).sizeof() == 4
        assert BytesInteger(4, signed=True).parse(b"\xff\xff\xff\xff") == -1
        assert BytesInteger(4, signed=True).build(-1) == b"\xff\xff\xff\xff"
        assert BytesInteger(4, swapped=True, bytesize=2).parse(b"\x00\xff\x00\x00") == 255
        assert BytesInteger(4, swapped=True, bytesize=2).build(255) == b"\x00\xff\x00\x00"
        assert BytesInteger(lambda ctx: 4).parse(b"\x00\x00\x00\xff") == 255
        assert BytesInteger(lambda ctx: 4).build(255) == b"\x00\x00\x00\xff"
        assert BytesInteger(lambda ctx: 4).sizeof() == 4

    def test_bitwise(self):
        assert Bitwise(Bytes(8)).parse(b"\xff") == b"\x01\x01\x01\x01\x01\x01\x01\x01"
        assert Bitwise(Bytes(8)).build(b"\x01\x01\x01\x01\x01\x01\x01\x01") == b"\xff"
        assert Bitwise(Bytes(8)).sizeof() == 1
        assert Bitwise(Bytes(lambda ctx: 8)).parse(b"\xff") == b"\x01\x01\x01\x01\x01\x01\x01\x01"
        assert Bitwise(Bytes(lambda ctx: 8)).build(b"\x01\x01\x01\x01\x01\x01\x01\x01") == b"\xff"
        assert Bitwise(Bytes(lambda ctx: 8)).sizeof() == 1

        assert Bitwise(Array(8,Bit)).parse(b"\xff") == [1,1,1,1,1,1,1,1]
        assert Bitwise(Array(8,Bit)).build([1,1,1,1,1,1,1,1]) == b"\xff"
        assert Bitwise(Array(2,Nibble)).parse(b"\xff") == [15,15]
        assert Bitwise(Array(2,Nibble)).build([15,15]) == b"\xff"
        assert Bitwise(Array(1,Octet)).parse(b"\xff") == [255]
        assert Bitwise(Array(1,Octet)).build([255]) == b"\xff"

    def test_bitstruct(self):
        assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "d"/BitsInteger(5)).parse(b"\xe1\x1f") == Container(a=7)(b=False)(c=8)(d=31)
        assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "d"/BitsInteger(5)).build(Container(a=7)(b=False)(c=8)(d=31)) == b"\xe1\x1f"
        assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "d"/BitsInteger(5)).sizeof() == 2
        assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "sub"/Struct("d"/Nibble, "e"/Bit)).parse(b"\xe1\x1f") == Container(a=7)(b=False)(c=8)(sub=Container(d=15)(e=1))
        assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "sub"/Struct("d"/Nibble, "e"/Bit)).sizeof() == 2
        assert BitStruct("a"/BitsInteger(3), "b"/Flag, Padding(3), "c"/Nibble, "sub"/Struct("d"/Nibble, "e"/Bit)).build(Container(a=7)(b=False)(c=8)(sub=Container(d=15)(e=1))) == b"\xe1\x1f"

    def test_embeddedbitstruct(self):
        d = Struct(
            "len" / Byte, 
            EmbeddedBitStruct("data" / BitsInteger(8)),
        )
        assert d.parse(b"\x08\xff") == Container(len=8)(data=255)
        assert d.build(dict(len=8,data=255)) == b"\x08\xff"
        assert d.sizeof() == 2

    def test_bitstruct_from_issue_39(self):
        d = Struct(
            "len" / Byte, 
            EmbeddedBitStruct("data" / BitsInteger(lambda ctx: ctx._.len)),
        )
        assert d.parse(b"\x08\xff") == Container(len=8)(data=255)
        assert d.build(dict(len=8,data=255)) == b"\x08\xff"
        assert raises(d.sizeof) == AttributeError

    def test_bytewise(self):
        assert Bitwise(Bytewise(Bytes(1))).parse(b"\xff") == b"\xff"
        assert Bitwise(Bytewise(Bytes(1))).build(b"\xff") == b"\xff"
        assert Bitwise(Bytewise(Bytes(1))).sizeof() == 1
        assert BitStruct(Nibble, "num"/Bytewise(Int24ub), Nibble).parse(b"\xf0\x10\x20\x3f") == Container(num=0x010203)
        assert Bitwise(Sequence(Nibble, Bytewise(Int24ub), Nibble)).parse(b"\xf0\x10\x20\x3f") == [0x0f,0x010203,0x0f]

    def test_byteswapped(self):
        assert ByteSwapped(Bytes(5)).parse(b"12345?????") == b"54321"
        assert ByteSwapped(Bytes(5)).build(b"12345") == b"54321"
        assert ByteSwapped(Bytes(5)).sizeof() == 5
        assert ByteSwapped(Struct("a"/Byte, "b"/Byte)).parse(b"\x01\x02") == Container(a=2)(b=1)
        assert ByteSwapped(Struct("a"/Byte, "b"/Byte)).build(Container(a=2)(b=1)) == b"\x01\x02"

    def test_byteswapped_from_issue_70(self):
        assert ByteSwapped(BitStruct("flag1"/Bit, "flag2"/Bit, Padding(2), "number"/BitsInteger(16), Padding(4))).parse(b'\xd0\xbc\xfa') == Container(flag1=1)(flag2=1)(number=0xabcd)
        assert BitStruct("flag1"/Bit, "flag2"/Bit, Padding(2), "number"/BitsInteger(16), Padding(4)).parse(b'\xfa\xbc\xd1') == Container(flag1=1)(flag2=1)(number=0xabcd)

    def test_bitsswapped(self):
        assert BitsSwapped(Bytes(2)).parse(b"\x0f\x01") == b"\xf0\x80"
        assert BitsSwapped(Bytes(2)).build(b"\xf0\x80") == b"\x0f\x01"
        assert Bitwise(Bytes(8)).parse(b"\xf2") == b'\x01\x01\x01\x01\x00\x00\x01\x00'
        assert BitsSwapped(Bitwise(Bytes(8))).parse(b"\xf2") == b'\x00\x01\x00\x00\x01\x01\x01\x01'
        assert BitStruct("a"/Nibble, "b"/Nibble).parse(b"\xf1") == Container(a=15)(b=1)
        assert BitsSwapped(BitStruct("a"/Nibble, "b"/Nibble)).parse(b"\xf1") == Container(a=8)(b=15)

    def test_bitsswapped_from_issue_145(self):
        def LBitStruct(*subcons):
            return BitsSwapped(BitStruct(*subcons))
        assert LBitStruct("num"/Octet).parse(b"\x01") == Container(num=0x80)

    def test_slicing(self):
        assert Slicing(Array(4,Byte), 4, 1, 3, empty=0).parse(b"\x01\x02\x03\x04") == [2,3]
        assert Slicing(Array(4,Byte), 4, 1, 3, empty=0).build([2,3]) == b"\x00\x02\x03\x00"
        assert Slicing(Array(4,Byte), 4, 1, 3, empty=0).sizeof() == 4

    def test_indexing(self):
        assert Indexing(Array(4,Byte), 4, 2, empty=0).parse(b"\x01\x02\x03\x04") == 3
        assert Indexing(Array(4,Byte), 4, 2, empty=0).build(3) == b"\x00\x00\x03\x00"
        assert Indexing(Array(4,Byte), 4, 2, empty=0).sizeof() == 4

    def test_select(self):
        assert raises(Select(Int32ub, Int16ub).parse, b"\x07") == SelectError
        assert Select(Int32ub, Int16ub, Int8ub).parse(b"\x07") == 7
        assert Select(Int32ub, Int16ub, Int8ub).build(7) == b"\x00\x00\x00\x07"
        assert Select("a"/Int32ub, "b"/Int16ub, "c"/Int8ub, includename=True).parse(b"\x07") == ("c", 7)
        assert Select("a"/Int32ub, "b"/Int16ub, "c"/Int8ub, includename=True).build((("c", 7))) == b"\x07"
        assert raises(Select("a"/Int32ub, "b"/Int16ub, "c"/Int8ub, includename=True).build, (("d", 7))) == SelectError
        assert raises(Select(Byte).sizeof) == SizeofError

    def test_peek(self):
        assert Peek(Int8ub).parse(b"\x01") == 1
        assert Peek(Int8ub).parse(b"") == None
        assert Peek(Int8ub).build(1) == b""
        assert Peek(Int8ub).build(None) == b""
        assert Peek(Int8ub).sizeof() == 0
        assert Peek(VarInt).sizeof() == 0
        assert Struct(Peek("a"/Int8ub), "b"/Int16ub).parse(b"\x01\x02") == Container(a=1)(b=0x0102)
        assert Struct(Peek("a"/Int8ub), "b"/Int16ub).build(dict(a=1,b=0x0102)) == b"\x01\x02"
        assert Struct(Peek("a"/Byte), Peek("b"/Int16ub)).parse(b"\x01\x02") == Container(a=1)(b=0x0102)
        assert Struct(Peek("a"/Byte), Peek("b"/Int16ub)).build(dict(a=0,b=0x0102)) == b""
        assert Struct(Peek("a"/Byte), Peek("b"/Int16ub)).sizeof() == 0

    def test_optional(self):
        assert Optional(Int32ul).parse(b"\x01\x00\x00\x00") == 1
        assert Optional(Int32ul).build(1) == b"\x01\x00\x00\x00"
        assert Optional(Int32ul).parse(b"???") == None
        assert Optional(Int32ul).build(None) == b""
        assert raises(Optional(Int32ul).sizeof) == SizeofError

    def test_union(self):
        assert Union("a"/Bytes(2), "b"/Int16ub).parse(b"\x01\x02") == Container(a=b"\x01\x02")(b=0x0102)
        assert Union("a"/Bytes(2), "b"/Int16ub).build(dict(a=b"zz"))  == b"zz"
        assert Union("a"/Bytes(2), "b"/Int16ub).build(dict(b=0x0102)) == b"\x01\x02"
        assert Union("a"/Bytes(2), "b"/Int16ub, buildfrom=0).build(dict(a=b"zz",b=5))  == b"zz"
        assert Union("a"/Bytes(2), "b"/Int16ub, buildfrom=1).build(dict(a=b"zz",b=5))  == b"\x00\x05"
        assert Union("a"/Bytes(2), "b"/Int16ub, buildfrom="a").build(dict(a=b"zz",b=5))  == b"zz"
        assert Union("a"/Bytes(2), "b"/Int16ub, buildfrom="b").build(dict(a=b"zz",b=5))  == b"\x00\x05"
        assert Union("a"/Bytes(2), "b"/Int16ub, buildfrom=Pass).build({}) == b""

        assert raises(Union(Byte).sizeof) == SizeofError
        assert raises(Union(VarInt).sizeof) == SizeofError
        assert Union(Byte, VarInt, buildfrom=0).sizeof() == 1
        assert raises(Union(Byte, VarInt, buildfrom=1).sizeof) == SizeofError

    def test_prefixedarray(self):
        assert PrefixedArray(Byte, Byte).parse(b"\x03\x01\x02\x03") == [1,2,3]
        assert PrefixedArray(Byte, Byte).parse(b"\x00") == []
        assert PrefixedArray(Byte, Byte).build([1,2,3]) == b"\x03\x01\x02\x03"
        assert raises(PrefixedArray(Byte, Byte).parse, b"") == ArrayError
        assert raises(PrefixedArray(Byte, Byte).parse, b"\x03\x01") == ArrayError
        assert raises(PrefixedArray(Byte, Byte).sizeof) == SizeofError

    def test_prefixed(self):
        assert Prefixed(Byte, Int16ul).parse(b"\x02\xff\xffgarbage") == 65535
        assert Prefixed(Byte, Int16ul).build(65535) == b"\x02\xff\xff"
        assert Prefixed(Byte, Int16ul).sizeof() == 3
        assert Prefixed(VarInt, GreedyBytes).parse(b"\x03abcgarbage") == b"abc"
        assert Prefixed(VarInt, GreedyBytes).build(b"abc") == b'\x03abc'
        assert Prefixed(Byte, Int64ub).sizeof() == 9
        assert raises(Prefixed(VarInt, GreedyBytes).sizeof) == SizeofError

    @pytest.mark.xfail(PY32 or PY33, reason="codecs module missing on some versions")
    def test_compressed(self):
        zeros = b"0" * 1000
        compressor = Compressed(GreedyBytes, "zlib")
        assert compressor.parse(compressor.build(zeros)) == zeros
        assert len(compressor.build(zeros)) == 17
        assert raises(compressor.sizeof) == SizeofError

        compressor = Compressed(Bytes(1000), "zlib")
        assert raises(compressor.sizeof) == SizeofError

    def test_string(self):
        assert String(5).parse(b"hello") == b"hello"
        assert String(5).build(b"hello") == b"hello"
        assert raises(String(5).parse, b"") == FieldError
        assert String(5).build(b"") == b"\x00\x00\x00\x00\x00"
        assert String(12, encoding="utf8").parse(b"hello joh\xd4\x83n") == u"hello joh\u0503n"
        assert String(12, encoding="utf8").build(u"hello joh\u0503n") == b"hello joh\xd4\x83n"
        assert String(12, encoding="utf8").sizeof() == 12
        assert raises(String(5).build, u"hello") == StringError    # missing encoding
        assert String(10, padchar=b"X", paddir="right").parse(b"helloXXXXX") == b"hello"
        assert String(10, padchar=b"X", paddir="left").parse(b"XXXXXhello") == b"hello"
        assert String(10, padchar=b"X", paddir="center").parse(b"XXhelloXXX") == b"hello"
        assert String(10, padchar=b"X", paddir="right").build(b"hello") == b"helloXXXXX"
        assert String(10, padchar=b"X", paddir="left").build(b"hello") == b"XXXXXhello"
        assert String(10, padchar=b"X", paddir="center").build(b"hello") == b"XXhelloXXX"
        assert raises(String, 10, padchar=u"X", encoding="utf8") == StringError     # missing encoding
        assert String(5, trimdir="right").build(b"1234567890") == b"12345"
        assert String(5, trimdir="left").build(b"1234567890") == b"67890"
        assert String(5, padchar=b"X", paddir="left", encoding="utf8").sizeof() == 5
        assert String(5).sizeof() == 5

    def test_pascalstring(self):
        assert PascalString(Byte).parse(b"\x05hello????????") == b"hello"
        assert PascalString(Byte).build(b"hello") == b"\x05hello"
        assert PascalString(Byte, encoding="utf8").parse(b"\x05hello") == u"hello"
        assert PascalString(Byte, encoding="utf8").build(u"hello") == b"\x05hello"
        assert PascalString(Int16ub).parse(b"\x00\x05hello????????") == b"hello"
        assert PascalString(Int16ub).build(b"hello") == b"\x00\x05hello"
        assert raises(PascalString(Byte).sizeof) == SizeofError
        assert raises(PascalString(VarInt).sizeof) == SizeofError

    def test_cstring(self):
        assert CString().parse(b"hello\x00") == b"hello"
        assert CString().build(b"hello") == b"hello\x00"
        assert CString(encoding="utf8").parse(b"hello\x00") == u"hello"
        assert CString(encoding="utf8").build(u"hello") == b"hello\x00"
        assert CString(terminators=b"XYZ", encoding="utf8").parse(b"helloX") == u"hello"
        assert CString(terminators=b"XYZ", encoding="utf8").parse(b"helloY") == u"hello"
        assert CString(terminators=b"XYZ", encoding="utf8").parse(b"helloZ") == u"hello"
        assert CString(terminators=b"XYZ", encoding="utf8").build(u"hello") == b"helloX"
        assert CString(encoding="utf16").build(u"hello") == b"\xff\xfeh\x00"
        assert raises(CString(encoding="utf16").parse, b'\xff\xfeh\x00') == UnicodeDecodeError
        assert raises(CString().sizeof) == SizeofError

    def test_greedystring(self):
        assert GreedyString().parse(b"hello\x00") == b"hello\x00"
        assert GreedyString().build(b"hello\x00") == b"hello\x00"
        assert GreedyString().parse(b"") == b""
        assert GreedyString().build(b"") == b""
        assert GreedyString(encoding="utf8").parse(b"hello\x00") == u"hello\x00"
        assert GreedyString(encoding="utf8").parse(b"") == u""
        assert GreedyString(encoding="utf8").build(u"hello\x00") == b"hello\x00"
        assert GreedyString(encoding="utf8").build(u"") == b""
        assert raises(GreedyString().sizeof) == SizeofError

    def test_globally_encoded_strings(self):
        setglobalstringencoding("utf8")
        assert String(20).build(u"Афон") == String(20, encoding="utf8").build(u"Афон")
        assert PascalString(VarInt).build(u"Афон") == PascalString(VarInt, encoding="utf8").build(u"Афон")
        assert CString().build(u"Афон") == CString(encoding="utf8").build(u"Афон")
        assert GreedyString().build(u"Афон") == GreedyString(encoding="utf8").build(u"Афон")
        setglobalstringencoding(None)

    def test_lazybound(self):
        assert LazyBound(lambda ctx: Byte).parse(b"\x01") == 1
        assert LazyBound(lambda ctx: Byte).build(1) == b"\x01"
        assert LazyBound(lambda ctx: Byte).sizeof() == 1

    def test_unknown(self):
        assert Struct("length" / Byte, "inner" / Struct("inner_length" / Byte, "data" / Bytes(lambda ctx: ctx._.length + ctx.inner_length))).parse(b"\x03\x02helloXXX") == Container(length=3)(inner=Container(inner_length=2)(data=b"hello"))
        assert Struct("length" / Byte, "inner" / Struct("inner_length" / Byte, "data" / Bytes(lambda ctx: ctx._.length + ctx.inner_length))).sizeof(Container(inner_length=2)(_=Container(length=3))) == 7

    def test_noneof(self):
        assert NoneOf(Byte,[4,5,6,7]).parse(b"\x08") == 8
        assert raises(NoneOf(Byte,[4,5,6,7]).parse, b"\x06") == ValidationError

    def test_oneof(self):
        assert OneOf(Byte,[4,5,6,7]).parse(b"\x05") == 5
        assert OneOf(Byte,[4,5,6,7]).build(5) == b"\x05"
        assert raises(OneOf(Byte,[4,5,6,7]).parse, b"\x08") == ValidationError
        assert raises(OneOf(Byte,[4,5,6,7]).build, 8) == ValidationError

    def test_hexdump(self):
        assert HexDump(Bytes(6)).parse(b'abcdef') == '0000   61 62 63 64 65 66                                 abcdef           \n'
        assert HexDump(Bytes(6)).build('0000   61 62 63 64 65 66                                 abcdef           \n') == b'abcdef'

    def test_lazystruct(self):
        assert LazyStruct().parse(b"") == Struct().parse(b"")
        assert LazyStruct().build({}) == Struct().build({})
        assert LazyStruct().sizeof() == Struct().sizeof()
        assert LazyStruct("a"/Byte, "b"/CString()).build(dict(a=1,b=b"abc")) == b"\x01abc\x00"
        assert raises(LazyStruct("a"/Byte, "b"/CString()).sizeof) == SizeofError
        assert LazyStruct("a"/Byte).build(dict(a=1)) == b"\x01"
        assert LazyStruct("a"/Byte).sizeof() == 1
        assert LazyStruct(Pass, Computed(lambda ctx: 0), Terminator).build(dict()) == b""
        assert LazyStruct(Pass, Computed(lambda ctx: 0), Terminator).sizeof() == 0
        assert LazyStruct("a"/Byte, "b"/LazyStruct("c"/Byte)).build(dict(a=1,b=dict(c=2))) == b"\x01\x02"
        assert LazyStruct().parse(b"") == dict()
        assert LazyStruct().build(dict()) == b""

        assert dict(LazyStruct("a"/Byte).parse(b"\x01")) == dict(a=1)
        assert LazyStruct("a"/Byte).build(dict(a=1)) == b"\x01"
        assert dict(LazyStruct("a"/Byte,"b"/CString()).parse(b"\x01abc\x00")) == dict(a=1,b=b"abc")
        assert LazyStruct("a"/Byte,"b"/CString()).build(dict(a=1,b=b"abc")) == b"\x01abc\x00"
        assert dict(LazyStruct(Pass, Computed(lambda ctx: 0), Terminator).parse(b"")) == dict()
        assert LazyStruct(Pass, Computed(lambda ctx: 0), Terminator).build(dict()) == b""

    def test_lazystruct_nested_embedded(self):
        assert dict(LazyStruct("a"/Byte,"b"/LazyStruct("c"/Byte)).parse(b"\x01\x02")) == dict(a=1,b=dict(c=2))
        assert LazyStruct("a"/Byte,"b"/LazyStruct("c"/Byte)).build(dict(a=1,b=dict(c=2))) == b"\x01\x02"
        assert dict(LazyStruct("a"/Byte,Embedded(LazyStruct("c"/Byte))).parse(b"\x01\x02")) == dict(a=1,c=2)
        assert LazyStruct("a"/Byte,Embedded(LazyStruct("c"/Byte))).build(dict(a=1,c=2)) == b"\x01\x02"

    def test_lazyrange(self):
        assert LazyRange(3,5,Byte).parse(b"\x01\x02\x03") == [1,2,3]
        assert LazyRange(3,5,Byte).parse(b"\x01\x02\x03\x04") == [1,2,3,4]
        assert LazyRange(3,5,Byte).parse(b"\x01\x02\x03\x04\x05") == [1,2,3,4,5]
        assert LazyRange(3,5,Byte).parse(b"\x01\x02\x03\x04\x05\x06") == [1,2,3,4,5]
        assert raises(LazyRange(3,5,Byte).parse, b"") == RangeError
        assert LazyRange(3,5,Byte).build([1,2,3]) == b"\x01\x02\x03"
        assert LazyRange(3,5,Byte).build([1,2,3,4]) == b"\x01\x02\x03\x04"
        assert LazyRange(3,5,Byte).build([1,2,3,4,5]) == b"\x01\x02\x03\x04\x05"
        assert raises(LazyRange(3,5,Byte).build, [1,2]) == RangeError
        assert raises(LazyRange(3,5,Byte).build, [1,2,3,4,5,6]) == RangeError
        assert raises(LazyRange(3,5,Byte).build, 0) == RangeError
        assert raises(LazyRange(3,5,Byte).sizeof) == SizeofError
        assert LazyRange(0,100,Struct("id"/Byte)).parse(b'\x01\x02') == [Container(id=1),Container(id=2)]
        assert LazyRange(0,100,Struct("id"/Byte)).build([dict(id=i) for i in range(5)]) == b'\x00\x01\x02\x03\x04'
        assert raises(LazyRange(0,100,Struct("id"/Byte)).build, dict(id=1)) == RangeError
        assert raises(LazyRange(0,100,Struct("id"/Byte)).sizeof) == SizeofError
        assert LazyRange(1,1,Byte).sizeof() == 1
        assert raises(LazyRange, -2, +7, Byte) == RangeError
        assert raises(LazyRange, -2, -7, Byte) == RangeError
        assert raises(LazyRange, +2, -7, Byte) == RangeError
        assert raises(LazyRange, 1, 1, VarInt) == SizeofError

        assert LazyRange(1,9,Byte).parse(b"12345") == Range(1,9,Byte).parse(b"12345")
        assert LazyRange(1,9,Byte).build([1,2,3]) == Range(1,9,Byte).build([1,2,3])

    def test_lazysequence(self):
        assert LazySequence(Int8ub, Int16ub).parse(b"\x01\x00\x02") == [1,2]
        assert LazySequence(Int8ub, Int16ub).build([1,2]) == b"\x01\x00\x02"
        assert LazySequence().parse(b"") == []
        assert LazySequence().build([]) == b""
        assert LazySequence().sizeof() == 0

        assert LazySequence(Int8ub,Int16ub).parse(b"\x01\x00\x02") == Sequence(Int8ub,Int16ub).parse(b"\x01\x00\x02")
        assert LazySequence(Int8ub,Int16ub).build([1,2]) == Sequence(Int8ub,Int16ub).build([1,2])
        assert LazySequence(Int8ub,Int16ub).sizeof() == Sequence(Int8ub,Int16ub).sizeof()

    def test_lazysequence_nested_embedded(self):
        assert LazySequence(Int8ub, Int16ub, LazySequence(Int8ub, Int8ub)).parse(b"\x01\x00\x02\x03\x04") == [1,2,[3,4]]
        assert LazySequence(Int8ub, Int16ub, LazySequence(Int8ub, Int8ub)).build([1,2,[3,4]]) == b"\x01\x00\x02\x03\x04"
        assert LazySequence(Int8ub, Int16ub, Embedded(LazySequence(Int8ub, Int8ub))).parse(b"\x01\x00\x02\x03\x04") == [1,2,3,4]
        assert LazySequence(Int8ub, Int16ub, Embedded(LazySequence(Int8ub, Int8ub))).build([1,2,3,4]) == b"\x01\x00\x02\x03\x04"

    def test_ondemand(self):
        assert OnDemand(Byte).parse(b"\x01garbage")() == 1
        assert OnDemand(Byte).build(1) == b"\x01"
        assert OnDemand(Byte).sizeof() == 1

        parseret = OnDemand(Byte).parse(b"\x01garbage")
        assert OnDemand(Byte).build(parseret) == b"\x01"

    def test_ondemandpointer(self):
        assert OnDemandPointer(lambda ctx: 2, Byte).parse(b"\x01\x02\x03garbage")() == 3
        assert OnDemandPointer(lambda ctx: 2, Byte).build(1) == b"\x00\x00\x01"
        assert OnDemandPointer(lambda ctx: 2, Byte).sizeof() == 0

    def test_from_issue_76(self):
        assert Aligned(Struct("a"/Byte, "f"/Bytes(lambda ctx: ctx.a)), modulus=4).parse(b"\x02\xab\xcd\x00") == Container(a=2)(f=b"\xab\xcd")
        assert Aligned(Struct("a"/Byte, "f"/Bytes(lambda ctx: ctx.a)), modulus=4).build(Container(a=2)(f=b"\xab\xcd")) == b"\x02\xab\xcd\x00"

    def test_flag(self):
        assert Flag.parse(b"\x00") == False
        assert Flag.parse(b"\x01") == True
        assert Flag.parse(b"\xff") == True
        assert Flag.build(False) == b"\x00"
        assert Flag.build(True) == b"\x01"
        assert Flag.sizeof() == 1

    def test_enum(self):
        assert Enum(Byte, q=3,r=4,t=5).parse(b"\x04") == "r"
        assert Enum(Byte, q=3,r=4,t=5).build("r") == b"\x04"
        assert Enum(Byte, q=3,r=4,t=5).build(4) == b"\x04"
        assert raises(Enum(Byte, q=3,r=4,t=5).parse, b"\x07") == MappingError
        assert raises(Enum(Byte, q=3,r=4,t=5).build, "spam") == MappingError
        assert Enum(Byte, q=3,r=4,t=5, default="spam").parse(b"\x07") == "spam"
        assert Enum(Byte, q=3,r=4,t=5, default=9).build("spam") == b"\x09"
        assert Enum(Byte, q=3,r=4,t=5, default=Pass).parse(b"\x07") == 7
        assert Enum(Byte, q=3,r=4,t=5, default=Pass).build(9) == b"\x09"
        assert Enum(Byte, q=3,r=4,t=5).sizeof() == 1

    def test_flagsenum(self):
        assert FlagsEnum(Byte, a=1,b=2,c=4,d=8,e=16,f=32,g=64,h=128).parse(b'\x81') == FlagsContainer(a=True,b=False,c=False,d=False,e=False,f=False,g=False,h=True)
        assert FlagsEnum(Byte, a=1,b=2,c=4,d=8,e=16,f=32,g=64,h=128).build(FlagsContainer(a=True,b=False,c=False,d=False,e=False,f=False,g=False,h=True)) == b'\x81'
        assert FlagsEnum(Byte, feature=4,output=2,input=1).parse(b'\x04') == FlagsContainer(output=False,feature=True,input=False)
        assert FlagsEnum(Byte, feature=4,output=2,input=1).build(dict(feature=True, output=True, input=False)) == b'\x06'
        assert FlagsEnum(Byte, feature=4,output=2,input=1).build(dict(feature=True)) == b'\x04'
        assert FlagsEnum(Byte, feature=4,output=2,input=1).build(dict()) == b'\x00'
        assert raises(FlagsEnum(Byte, feature=4,output=2,input=1).build, dict(unknown=True)) == MappingError

    @pytest.mark.xfail(PYPY, reason="numpy not on Travis pypy")
    def test_numpy(self):
        import numpy
        obj = numpy.array([1,2,3], dtype=numpy.int64)
        assert numpy.array_equal(Numpy.parse(Numpy.build(obj)), obj)

    def test_restreamed(self):
        assert Restreamed(Int16ub, ident, 1, ident, 1, ident).parse(b"\x00\x01") == 1
        assert Restreamed(Int16ub, ident, 1, ident, 1, ident).build(1) == b"\x00\x01"
        assert Restreamed(Int16ub, ident, 1, ident, 1, ident).sizeof() == 2
        assert raises(Restreamed(VarInt, ident, 1, ident, 1, ident).sizeof) == SizeofError
        assert Restreamed(Bytes(2), None, None, lambda b: b*2, 1, None).parse(b"a") == b"aa"
        assert Restreamed(Bytes(1), lambda b: b*2, 1, None, None, None).build(b"a") == b"aa"
        assert Restreamed(Bytes(5), None, None, None, None, lambda n: n*2).sizeof() == 10
        print("Note: tested mosty as Bitwise and Bytewise")

    def test_rebuffered(self):
        data = b"0" * 1000
        assert Rebuffered(Array(1000,Byte)).parse_stream(BytesIO(data)) == [48]*1000
        assert Rebuffered(Array(1000,Byte), tailcutoff=50).parse_stream(BytesIO(data)) == [48]*1000

    def test_expradapter(self):
        MulDiv = ExprAdapter(Byte,
            encoder = lambda obj,ctx: obj // 7,
            decoder = lambda obj,ctx: obj * 7, )

        assert MulDiv.parse(b"\x06") == 42
        assert MulDiv.build(42) == b"\x06"
        assert MulDiv.sizeof() == 1

        Ident = ExprAdapter(Byte,
            encoder = lambda obj,ctx: obj+1,
            decoder = lambda obj,ctx: obj-1, )

        assert Ident.parse(b"\x02") == 1
        assert Ident.build(1) == b"\x02"
        assert Ident.sizeof() == 1

    def test_ipaddress(self):
        class IpAddressAdapter(Adapter):
            def _encode(self, obj, context):
                return list(map(int, obj.split(".")))
            def _decode(self, obj, context):
                return "{0}.{1}.{2}.{3}".format(*obj)
        IpAddress = IpAddressAdapter(Byte[4])

        assert IpAddress.parse(b"\x7f\x80\x81\x82") == "127.128.129.130"
        assert IpAddress.build("127.1.2.3") == b"\x7f\x01\x02\x03"
        assert IpAddress.sizeof() == 4

        IpAddress = ExprAdapter(Byte[4], 
            encoder = lambda obj,ctx: list(map(int, obj.split("."))),
            decoder = lambda obj,ctx: "{0}.{1}.{2}.{3}".format(*obj), )

        assert IpAddress.parse(b"\x7f\x80\x81\x82") == "127.128.129.130"
        assert IpAddress.build("127.1.2.3") == b"\x7f\x01\x02\x03"
        assert IpAddress.sizeof() == 4

    def test_lazybound_node(self):
        print("need some ideas how to test it")
        Node = Struct(
            "value" / Int8ub,
            "next" / LazyBound(lambda ctx: Node), )

    def test_checksum(self):
        def sha512(b):
            return hashlib.sha512(b).digest()
        d = Struct(
            "fields" / RawCopy(Struct(
                "a" / Byte,
                "b" / Byte,
            )),
            "checksum" / Checksum(Bytes(64), sha512, "fields"),
        )

        c = sha512(b"\x01\x02")
        assert d.parse(b"\x01\x02"+c) == Container(fields=dict(data=b"\x01\x02", value=Container(a=1)(b=2), offset1=0, offset2=2, length=2))(checksum=c)
        assert d.build(dict(fields=dict(data=b"\x01\x02"))) == b"\x01\x02"+c
        assert d.build(dict(fields=dict(value=dict(a=1,b=2)))) == b"\x01\x02"+c

    def test_from_issue_60(self):
        Header = Struct(
            "type" / Int8ub,
            "size" / Switch(lambda ctx: ctx.type,
            {
                0: Int8ub,
                1: Int16ub,
                2: Int32ub,
            }),
            "length" / Tell,
        )
        assert Header.parse(b"\x00\x05")             == Container(type=0)(size=5)(length=2)
        assert Header.parse(b"\x01\x00\x05")         == Container(type=1)(size=5)(length=3)
        assert Header.parse(b"\x02\x00\x00\x00\x05") == Container(type=2)(size=5)(length=5)
        assert Header.build(dict(type=0, size=5)) == b"\x00\x05"
        assert Header.build(dict(type=1, size=5)) == b"\x01\x00\x05"
        assert Header.build(dict(type=2, size=5)) == b"\x02\x00\x00\x00\x05"

        HeaderData = Struct(
            Embedded(Header),
            "data" / Bytes(lambda ctx: ctx.size),
        )
        assert HeaderData.parse(b"\x00\x0512345")             == Container(type=0)(size=5)(length=2)(data=b"12345")
        assert HeaderData.parse(b"\x01\x00\x0512345")         == Container(type=1)(size=5)(length=3)(data=b"12345")
        assert HeaderData.parse(b"\x02\x00\x00\x00\x0512345") == Container(type=2)(size=5)(length=5)(data=b"12345")
        assert HeaderData.build(dict(type=0, size=5, data=b"12345")) == b"\x00\x0512345"
        assert HeaderData.build(dict(type=1, size=5, data=b"12345")) == b"\x01\x00\x0512345"
        assert HeaderData.build(dict(type=2, size=5, data=b"12345")) == b"\x02\x00\x00\x00\x0512345"

    def test_struct_proper_context(self):
        d1 = Struct(
            "x"/Byte,
            "inner"/Struct(
                "y"/Byte,
                "a"/Computed(this._.x+1),
                "b"/Computed(this.y+2),
            ),
            "c"/Computed(this.x+3),
            "d"/Computed(this.inner.y+4),
        )
        d2 = Struct(
            "x"/Byte,
            "inner"/Embedded(Struct(
                "y"/Byte,
                "a"/Computed(this._.x+1),  # important
                "b"/Computed(this.y+2),    # important
            )),
            "c"/Computed(this.x+3),
            "d"/Computed(this.y+4),
        )
        assert d1.parse(b"\x01\x0f") == Container(x=1)(inner=Container(y=15)(a=2)(b=17))(c=4)(d=19)
        # a-field computed on nested context, merged only after entire inner-struct returns
        assert d2.parse(b"\x01\x0f") == Container(x=1)(y=15)(a=2)(b=17)(c=4)(d=19)


