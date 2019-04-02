#!/bin/sh

main() {
    local line
    local app
    local code
    while read line; do
        app="${line//   *}"
        code="${line//* }"
        echo "[$app][$code]"
        if curl -XDELETE -H "From:$app" "$(hostname):8040/api/file/${code}"; then
            echo "[succ][$app][$code]"
        else
            echo "[fail][$app][$code]"
        fi
    done < wiki.lst
}

main "$@"
