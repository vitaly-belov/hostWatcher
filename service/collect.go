// Copyright 2012 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

//go:build windows

package main

import (
	"syscall"
)

var (
	collectFunc = syscall.MustLoadDLL("user32.dll").MustFindProc("MessageBeep")
)

func collect() {
	collectFunc.Call(0xffffffff)
}
