function loadSafe() {
    /**
     * 保存原始对象
     * 所有对象通过 g + 原始属性进行访问
     * */

    function propertyExists(p) {
        /**
         * 判断属性是否在 window 上
         * */
        return Object.getOwnPropertyDescriptor(window, p)
    }

    // 判断属性是否存在并注入自己的属性
    if (!propertyExists('gprint')) {
        window.gprint = console.log;
    }
    if (!propertyExists('gwindow')) {
        window.gwindow = window;
    }
    if (!propertyExists('gdocument')) {
        window.gdocument = document;
    }

    window.gHasHook = true; // 做一个标志防止重复操作
}

function hookCookie(cookie) {
    /**
     * hook cookie
     * */
    let cookieCache = gdocument.cookie;

    Object.defineProperty(gdocument, 'cookie', {
        get() {
            gprint("获取 cookie：", cookieCache);
            return cookieCache
        },
        set(v) {
            if (cookie && c.match(cookie + '=')) debugger;

            gprint("设置 cookie：", v);
            cookieCache = v;
        }
    })
}

(() => {
    if (!Object.getOwnPropertyDescriptor(window, 'gHasHook')) {
        loadSafe();

        hookCookie();
    }
})();