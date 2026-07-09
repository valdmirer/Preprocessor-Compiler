"section .data"
	"newline db 10"
	"space db 32"
	"tab db 9"
	"null db 0"
.F1323:
	"paddq " + a + ", " + b
"_start:"
	"call main"
	"mov rdi, rax"
	"mov rax, 60"
	"syscall"
.F1275:
	"test " + condition
	"jz .assert_fail"
".assert_ok:"
	"nop"
"section .text"
	"global _" + name
	"_" + name + ":"
	"push rbp"
	"mov rbp, rsp"
.F2612:
	"; COMPILATION COMPLETE"
	"; GENERATED ASSEMBLY READY FOR NASM/YASM"