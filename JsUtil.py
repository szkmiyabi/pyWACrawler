class JsUtil:

    @staticmethod
    def image_alt():
        return '''
            var fname_flg = true;
            var img = document.getElementsByTagName("img");
            for(var i=0; i<img.length; i++) {
                var imgtag = img.item(i);
                imgtag.setAttribute("style", "border:1px solid red;");
                var span_id = "bkm-img-span-" + i;
                var src_val = imgtag.getAttribute("src");
                var fname = get_img_filename(src_val);
                var alt_val = imgtag.getAttribute("alt");
                if(alt_val === null) {
                    alt_val = alt_attr_from_dirtycode(imgtag);
                }
                var html_str = "";
                if(alt_attr_check(imgtag)) {
                    html_str += "alt: " + alt_val;
                } else {
                    html_str += "alt属性がない";
                }
                if(fname_flg) {
                    if(html_str !== "") {
                        html_str += ", filename: " + fname;
                    } else {
                        html_str += "filename: " + fname;
                    }
                }
                var css_txt = "color:#fff;font-size:12px;padding:1px;background:#BF0000;";
                var span = '<span id="' + span_id + '" style="' + css_txt + '">' + html_str + '</span>';
                imgtag.insertAdjacentHTML("beforebegin", span);
            }
            tag_link_img();
            function alt_attr_from_dirtycode(obj) {
                var ret = "";
                var imgtag = obj.outerHTML;
                var pt = new RegExp('(alt=")(.*?)(")');
                if(pt.test(imgtag)) {
                    ret = imgtag.match(pt)[2];
                }
                return ret;
            }
            function get_img_filename(str) {
                var ret = "";
                var pat = new RegExp("(.+)\/(.+\.)(JPG|jpg|GIF|gif|PNG|png|BMP|bmp)$");
                if(pat.test(str)) {
                    var arr = str.match(pat);
                    ret += arr[2] + arr[3];
                }
                return ret;
            }
            function alt_attr_check(imgtag) {
                var txt = imgtag.outerHTML;
                var pt1 = new RegExp('alt=".*"');
                var pt2 = new RegExp('alt=');
                if(pt1.test(txt) && pt2.test(txt)) return true;
                else return false;
            }
            function tag_link_img() {
                var ats = document.getElementsByTagName("a");
                var css_txt = "border:2px dotted red;";
                for(var i=0; i<ats.length; i++) {
                    var atag = ats.item(i);
                    var imgs = atag.getElementsByTagName("img");
                    for(var j=0; j<imgs.length; j++) {
                        var img = imgs.item(j);
                        img.setAttribute("style", css_txt);
                    }
                }
            }
        '''
    
    @staticmethod
    def target_attr():
        return '''
                        var ats = document.getElementsByTagName("a");
            for(var i=0; i<ats.length; i++) {
                var atag = ats.item(i);
                var ataghtml = atag.outerHTML;
                ataghtml = _text_clean(ataghtml);
                if(_target_attr_check(ataghtml)) {
                    var target_vl = atag.getAttribute("target");
                    var span_id = "bkm-target-attr-span-" + i;
                    var span_html = (target_vl === "") ? "target属性有:(空)" : "target属性有:" + target_vl;
                    var span_css = "padding-right:5px;color:#fff;font-size:12px;padding:1px;background:#008000;border-radius:5px;";
                    var span = '<span id="' + span_id + '" style="' + span_css + '">' + span_html + '</span>';
                    atag.insertAdjacentHTML("beforebegin", span);
                }
            }
            function _target_attr_check(str) {
                var pt = new RegExp('target=".*?"');
                if(pt.test(str)) return true;
                else return false;
            }
            function _text_clean(str) {
                var ret = "";
                ret = str.replace(new RegExp("^ +", "mg"), "");
                ret = ret.replace(new RegExp("\\t+", "mg"), "");
                ret = ret.replace(new RegExp("(\\r\\n|\\r|\\n)", "mg"), "");
                return str;
            }
        '''