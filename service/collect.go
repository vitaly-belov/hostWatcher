// Copyright 2012 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

//go:build windows

package main

import (
	"syscall"
)

// BUG(brainman): MessageBeep Windows api is broken on Windows 7,
// so this example does not beep when runs as service on Windows 7.

var (
	collectFunc = syscall.MustLoadDLL("user32.dll").MustFindProc("MessageBeep")
)

func collect() {
	collectFunc.Call(0xffffffff)
}
