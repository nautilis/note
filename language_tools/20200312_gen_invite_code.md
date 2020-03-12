## 生成邀请码
```golang
package commonTest

import (
	"fmt"
	"math/rand"
	"testing"
)

var BASE = []byte{'H', 'V', 'E', '8', 'S', '2', 'D', 'Z', 'X', '9', 'C', '7', 'P',
	'5', 'I', 'K', '3', 'M', 'J', 'U', 'F', 'R', '4', 'W', 'Y', 'L', 'T', 'N', '6', 'B', 'G', 'Q'}

var SUFFIX_CHAR = byte('A')

func genCode(uid int64, codeLen int64) string {
	buf := make([]byte, 32)
	position := 32
	for uid/32 > 0 {
		index := uid % 32
		position -= 1
		buf[position] = BASE[index]
		uid /= 32
	}

	position -= 1
	buf[position] = BASE[uid%32]
	res := string(buf[position:])

	currentLen := int64(len(res))
	if currentLen < codeLen {
		sb := []byte{}
		sb = append(sb, SUFFIX_CHAR)
		for i := int64(0); i < codeLen-currentLen-1; i++ {
			sb = append(sb, BASE[rand.Intn(32)])
		}
		res += string(sb)
	}
	return res
}

func getUidFromCode(code string) int64 {
	charList := []byte(code)
	result := 0
	for i := 0; i < len(charList); i++ {
		index := 0
		for j := 0; j < 32; j++ {
			if charList[i] == BASE[j] {
				index = j
				break
			}
		}
		if charList[i] == SUFFIX_CHAR {
			break
		}

		if i > 0 {
			result = result*32 + index
		} else {
			result = index
		}
	}
	return int64(result)

}

func TestGenCode(t *testing.T) {
	code1 := genCode(100000, 6)
	code6 := genCode(100064, 6)
	code2 := genCode(100000000, 6)
	code3 := genCode(99999999, 6)
	code4 := genCode(99999989, 6)
	code5 := genCode(999999999, 6)
	t.Log(code1)
	t.Log(code6)
	t.Log(code2)
	t.Log(code3)
	t.Log(code4)
	t.Log(code5)
	for i := int64(999999100); i < int64(999999999); i++ {
		code := genCode(i, 6)
		uid := getUidFromCode(code)
		if uid != i {
			t.Log(fmt.Sprintf("uid not match code code => %s, uid => %d, i=>%d", code, uid, i))
		} else {
			t.Log("equal")
		}
	}
}
```
