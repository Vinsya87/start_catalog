document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".copy-button").forEach(function (e) {
    e.addEventListener("click", function () {
      var e = this.getAttribute("data-clipboard-target"),
        t = document.querySelector(e),
        r = document.createRange();
      r.selectNode(t),
        window.getSelection().removeAllRanges(),
        window.getSelection().addRange(r);
      try {
        document.execCommand("copy");
      } catch (a) {
        alert("Ошибка копирования: ", a);
      }
      window.getSelection().removeAllRanges();
    });
  });
});
document.getElementById("offcan_in").addEventListener("click", function () {
  var offcanMain = document.getElementById("offcan_main");
  offcanMain.classList.toggle("show");
});
document.getElementById("offcan_off").addEventListener("click", function () {
  var offcanMain = document.getElementById("offcan_main");
  offcanMain.classList.remove("show");
});
const swiper = new Swiper(".swiper", {
    loop: !0,
    slidesPerView: 1,
    // autoplay: { delay: 4e3, pauseOnMouseEnter: !0 },
    pagination: { el: ".swiper-pagination" },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    scrollbar: { el: ".swiper-scrollbar" },
  }),
  hits_main_parent = new Swiper(".hits_main_parent", {
    autoplay: { delay: 3e3, pauseOnMouseEnter: !0 },
    lazy: !0,
    pagination: { el: ".swiper-pagination", clickable: !0 },
    navigation: { nextEl: ".index-next", prevEl: ".index-prev" },
    slidesPerView: 6,
    grabCursor: !0,
    spaceBetween: 20,
    breakpoints: {
      1200: { spaceBetween: 10, slidesPerView: 6 },
      992: { slidesPerView: 4, spaceBetween: 10 },
      768: { slidesPerView: 3, spaceBetween: 10 },
      500: { slidesPerView: 2, loop: !0 },
      300: { slidesPerView: 1, loop: !0 },
    },
  }),
  reviews_index_main = new Swiper(".reviews_index_main", {
    autoplay: { delay: 3e3, pauseOnMouseEnter: !0 },
    lazy: !0,
    pagination: { el: ".swiper-pagination", clickable: !0 },
    navigation: { nextEl: ".arrow-next", prevEl: ".arrow-prev" },
    slidesPerView: 4,
    grabCursor: !0,
    spaceBetween: 20,
    breakpoints: {
      992: { spaceBetween: 10 },
      768: { slidesPerView: 3, spaceBetween: 10 },
      500: { slidesPerView: 2, loop: !0 },
      300: { slidesPerView: 1, loop: !0 },
    },
  }),
  headerItemDivs = document.querySelectorAll(".header_item_div_main");
headerItemDivs.forEach((e) => {
  e.addEventListener("mouseover", () => {
    e.classList.add("active");
  }),
    e.addEventListener("mouseout", () => {
      e.classList.remove("active");
    });
}),
  $(document).ready(function () {
    $(".lk_top_sign").click(function () {
      $("#authModal").toggleClass("active");
    }),
      $(".active_script").click(function () {
        $(this).toggleClass("active");
      }),
      $(".active_parent").click(function () {
        $(this).parent().toggleClass("active");
      });
  }),
  $(".primary_btn").click(function () {
    var e = $(this).attr("id").replace("-btn", ""),
      t = $("#" + e),
      r = t.hasClass("active");
    if (
      (r ||
        ($(".primary_btn").removeClass("active"), $(this).addClass("active")),
      $(".primary_desc").removeClass("active"),
      r)
    )
      t.removeClass("active"), $(this).removeClass("active");
    else {
      t.addClass("active");
      var a = $("#desc").offset().top;
      $("html, body").scrollTop(a - 80);
    }
  }),
  $(window).scroll(function () {
    var e = $(window).height(),
      t = $(window).scrollTop();
    $(".primary_desc_main").each(function () {
      var r = $(this).offset().top,
        a = $(this).outerHeight();
      t + e >= r + a - 250
        ? ($(this).addClass("active"), $(".primary_block").addClass("active"))
        : ($(this).removeClass("active"),
          $(".primary_block").removeClass("active"));
    });
  }),
  $(document).ready(function () {
    $(".btn_no").click(function () {
      $(".div_101_p").removeClass("active"),
        $(".btn_all").removeClass("active"),
        $(this).removeClass("active");
    });
  }),
  $(document).ready(function () {
    $(".write_me").click(function () {
      $("#write_me").toggleClass("active");
    });
  }),
  $(document).ready(function () {
    $(".show_more_review").click(function () {
      $("#review_full").toggleClass("active");
    });
  }),
  $(document).ready(function () {
    $(".close_modal").click(function () {
      $(".modal_reg").removeClass("active");
    });
  }),
  $(document).ready(function () {
    $(".review_write_btn").click(function () {
      $("#review_write").addClass("active");
    });
  });
const headerDownMain = document.querySelector(".header_down_main_none");
window.addEventListener("scroll", function () {
  window.pageYOffset >= 300 && !headerDownMain.classList.contains("active")
    ? headerDownMain.classList.add("active")
    : window.pageYOffset < 300 &&
      headerDownMain.classList.contains("active") &&
      headerDownMain.classList.remove("active");
}),
  $(document).ready(function () {
    $(".category_pod, .category_item").hide(),
      $(".cat_gl").click(function () {
        $(".category_pod, .category_item")
          .not($(this).nextAll(".category_pod, .category_item"))
          .slideUp(),
          $(this).next(".category_pod").slideToggle();
      }),
      $(".category_pod p").click(function () {
        $(".category_item").not($(this).next(".category_item")).slideUp(),
          $(this).next(".category_item").slideToggle();
      });
  });
var form = document.getElementById("writeForm_2");
function submitForm(e) {
  var t = e.attr("action"),
    r = e.serialize();
  (r += "&username=" + encodeURIComponent($("#id_name").val())),
    $.ajax({
      url: t,
      type: "POST",
      data: r,
      success: function (t) {
        e.trigger("reset"),
          $("#review_write").removeClass("active"),
          $("#review_ok").addClass("active");
      },
      error: function (e) {
        var t = e.responseJSON.errors,
          r = "";
        for (var a in t) r += "<p>" + t[a] + "</p>";
        $("#review-form-errors").html(r);
      },
    });
}
form &&
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var t = new XMLHttpRequest();
    t.open("POST", form.action),
      t.setRequestHeader(
        "X-CSRFToken",
        form.querySelector("[name=csrfmiddlewaretoken]").value
      ),
      (t.onreadystatechange = function () {
        if (4 === t.readyState) {
          if (200 === t.status)
            setTimeout(function () {
              document.querySelector("#write_me").classList.remove("active"),
                document.querySelector("#write_ok").classList.add("active");
            }, 500),
              form.reset();
          else if (400 === t.status) {
            var e = JSON.parse(t.responseText),
              r = e.errors;
            if (r) {
              var a = "";
              for (var o in r) a += decodeURIComponent(r[o]);
              document.querySelector(".error_login").textContent = a;
            }
          } else if (500 === t.status) {
            var e = JSON.parse(t.responseText),
              a = e.errors;
            alert(a);
          } else alert("Ошибка отправки сообщения");
        }
      });
    var r = new FormData(form);
    t.send(r);
  }),
  $(document).ready(function () {
    $("#review-form").submit(function (e) {
      e.preventDefault(), submitForm($(this));
    });
  }),
  $(document).ready(function () {
    $(".show_more_review").click(function (e) {
      e.preventDefault();
      var t = $(this).data("review-id");
      $.ajax({
        url: "/reviews/get_full_review/",
        data: { review_id: t },
        success: function (e) {
          var t = e.review;
          $("#review_full .review_date").text(t.created_at),
            $("#review_full .review_name").text(t.name),
            $("#review_full .review_text").text(t.text);
        },
      });
    });
  });
const favoriteForms = document.querySelectorAll(".favorite-form"),
  numFavoriteProductsElements = document.querySelectorAll(
    ".favorite_products_num"
  );
let num_favorite_products = parseInt(
  numFavoriteProductsElements[0].textContent
);
favoriteForms.forEach((e) => {
  e.addEventListener("submit", (t) => {
    t.preventDefault(), e.querySelector(".add-to-favorite-btn");
    let r = e.querySelector(".wish_prod"),
      a = e.getAttribute("action"),
      o = new FormData(e),
      s = r.querySelector("p");
    return (
      fetch(a, {
        method: "POST",
        body: o,
        headers: { "X-CSRFToken": "{{ csrf_token }}" },
      })
        .then((e) => e.json())
        .then((e) => {
          e.added
            ? (r.classList.add("active"),
              (num_favorite_products += 1),
              s && (s.textContent = "В избранном"))
            : (r.classList.remove("active"),
              (num_favorite_products -= 1),
              s && (s.textContent = "В избранное")),
            numFavoriteProductsElements.forEach((e) => {
              e.textContent = num_favorite_products;
            });
        })
        .catch((e) => {
          console.error(e);
        }),
      !1
    );
  });
}),
  document.addEventListener("DOMContentLoaded", function () {
    var e = document.querySelector("#lk_top_login"),
      t = document.querySelector("#login_in");
    e.addEventListener("mouseover", function () {
      t.classList.add("active");
    }),
      t.addEventListener("mouseleave", function () {
        t.classList.remove("active");
      });
  }),
  document.addEventListener("DOMContentLoaded", function () {
    var e = document.querySelector("#lk_top_login_min"),
      t = document.querySelector("#login_in_min");
    e.addEventListener("mouseover", function () {
      t.classList.add("active");
    }),
      t.addEventListener("mouseleave", function () {
        t.classList.remove("active");
      });
  }),
  $(document).ready(function () {
    $(".form_group_reg").click(function () {
      $("#authModal").removeClass("active"),
        $("#authModalreg").addClass("active");
    });
  }),
  $(document).ready(function () {
    $(".span_prev").click(function () {
      $("#authModalreg").removeClass("active"),
        $("#authModal").addClass("active");
    });
  }),
  document.addEventListener("DOMContentLoaded", function () {
    let e = document.getElementById("regForm");
    e &&
      e.addEventListener("submit", function (t) {
        t.preventDefault();
        let r = new XMLHttpRequest(),
          a = new FormData(e),
          o = e.getAttribute("method"),
          s = e.getAttribute("action");
        r.open(o, s, !0),
          r.setRequestHeader("X-CSRFToken", a.get("csrfmiddlewaretoken")),
          (r.onload = function () {
            if (200 === r.status) {
              let t = JSON.parse(r.responseText);
              if (t.success)
                t.activation_required
                  ? (document
                      .querySelector("#authModalreg")
                      .classList.remove("active"),
                    alert(
                      "Требуется активация учетной записи. Обратитесь к администратору."
                    ))
                  : (document
                      .querySelector("#authModalreg")
                      .classList.remove("active"),
                    window.location.reload());
              else {
                let a = e.querySelector(".error_login");
                (a.innerHTML = t.message), (a.style.display = "block");
              }
            } else {
              let o = e.querySelector(".error_login");
              (o.textContent = "Ошибка на сервере. Статус код: " + r.status),
                (o.style.display = "block");
            }
          }),
          r.send(a);
      });
  });
const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value,
  logoutForms = document.querySelectorAll(".logout-form");
logoutForms.forEach((e) => {
  e.addEventListener("submit", function (t) {
    t.preventDefault();
    let r = new XMLHttpRequest();
    r.open("POST", e.action),
      r.setRequestHeader("X-CSRFToken", csrfToken),
      (r.onreadystatechange = function () {
        if (r.readyState === XMLHttpRequest.DONE && 200 === r.status) {
          let e = JSON.parse(r.responseText);
          e.success && (window.location.href = "/");
        }
      }),
      r.send();
  });
}),
  document.querySelector("#authForm").addEventListener("submit", function (e) {
    e.preventDefault();
    let t = e.target,
      r = new FormData(t),
      a = new XMLHttpRequest();
    a.open("POST", t.action),
      a.setRequestHeader("X-CSRFToken", r.get("csrfmiddlewaretoken")),
      (a.onreadystatechange = function () {
        if (a.readyState === XMLHttpRequest.DONE) {
          if (200 === a.status) {
            let e = JSON.parse(a.responseText);
            if (e.success)
              document.querySelector(".modal_reg").classList.remove("active"),
                window.location.reload();
            else {
              let r = t.querySelector(".error_login");
              (r.textContent = e.message), (r.style.display = "block");
            }
          } else {
            let o = t.querySelector(".error_login");
            (o.textContent = "Ошибка на сервере"), (o.style.display = "block");
          }
        }
      }),
      a.send(r);
  }),
  $(document).ready(function () {
    $('form[id^="form_active_moneybox_"]').on("submit", function (e) {
      e.preventDefault();
      var t = $(this),
        r = t.attr("action"),
        a = t.serialize();
      $.ajax({
        type: "POST",
        url: r,
        data: a,
        dataType: "json",
        success: function (e) {
          var r = t.find(".message_moneybox");
          e.message
            ? (r.html('<p class="message_moneybox">' + e.message + "</p>"),
              (window.location.href = "/moneybox/"))
            : e.error &&
              r.html('<p class="message_moneybox">' + e.error + "</p>");
        },
        error: function () {
          t.find(".message_moneybox").html(
            '<p class="error-message">Произошла ошибка на сервере.</p>'
          );
        },
      });
    });
  }),
  $(document).ready(function () {
    $('form[id^="update_piggybank_form_"]').on("submit", function (e) {
      e.preventDefault();
      var t = $(this),
        r = t.attr("action"),
        a = t.serialize();
      $.ajax({
        type: "POST",
        url: r,
        data: a,
        dataType: "json",
        success: function (e) {
          var r = t.find(".message_moneybox");
          e.message
            ? r.html('<p class="success-message">' + e.message + "</p>")
            : e.error && r.html('<p class="error-message">' + e.error + "</p>");
        },
        error: function () {
          t.find(".message_moneybox").html(
            '<p class="error-message">Произошла ошибка на сервере.</p>'
          );
        },
      });
    });
  }),
  document.addEventListener("DOMContentLoaded", function () {
    document
      .querySelector(".form_balance")
      .addEventListener("submit", function (e) {
        confirm("Пополнить баланс?") || e.preventDefault();
      });
  }),
  $(document).ready(function () {
    $("#up_piggybank").on("submit", function (e) {
      if (confirm("Пополнить копилку?")) {
        e.preventDefault();
        var t = $(this),
          r = t.attr("action"),
          a = t.serialize();
        $.ajax({
          type: "POST",
          url: r,
          data: a,
          dataType: "json",
          success: function (e) {
            var r = t.find(".message_moneybox");
            e.success
              ? (r.html('<p class="success-message">' + e.success + "</p>"),
                setTimeout(function () {
                  location.reload(!0);
                }, 1e3))
              : e.error &&
                r.html('<p class="error-message">' + e.error + "</p>");
          },
          error: function () {
            t.find(".message_moneybox").html(
              '<p class="error-message">Произошла ошибка на сервере.</p>'
            );
          },
        });
      } else e.preventDefault();
    });
  });
const basketForms = document.querySelectorAll(".basket-form"),
  numBasketProductsElements = document.querySelectorAll(".basket_products_num");
let num_basket_products = parseInt(numBasketProductsElements[0].textContent);
function confirmDelete(e) {
  confirm("Вы уверены, что хотите удалить?") &&
    document.getElementById("delete_piggybank_" + e).submit();
}
basketForms.forEach((e) => {
  e.addEventListener("submit", (t) => {
    t.preventDefault(), e.querySelector(".add-to-basket-btn");
    let r = e.querySelector(".basket_prod"),
      a = e.getAttribute("action"),
      o = new FormData(e),
      s = r.querySelector("p");
    return (
      console.log("Button clicked"),
      fetch(a, {
        method: "POST",
        body: o,
        headers: { "X-CSRFToken": "{{ csrf_token }}" },
      })
        .then((e) => e.json())
        .then((e) => {
          console.log(e),
            e.added
              ? (r.classList.add("active"),
                (num_basket_products += 1),
                s && (s.textContent = "В корзине"))
              : (r.classList.remove("active"),
                (num_basket_products -= 1),
                s && (s.textContent = "В корзину")),
            numBasketProductsElements.forEach((e) => {
              e.textContent = num_basket_products;
            });
        })
        .catch((e) => {
          console.error(e);
        }),
      !1
    );
  });
}),
  $(document).ready(function () {
    $(".dropdown_item_count").click(function (e) {
      e.preventDefault();
      var t = $(this).data("value");
      $("#show_count").text(t),
        $("#show_count_input").val(t),
        $(this).removeAttr("data-value"),
        $(".form_sort_show").submit();
    });
  }),
  $(document).ready(function () {
    $(".dropdown_sort").click(function (e) {
      e.preventDefault();
      var t = $(this).data("value");
      $("#show_sort").text($(this).text()),
        $("#show_sort_input").val(t),
        $(this).removeAttr("data-value"),
        $(".form_sort_price").submit();
    });
  }),
  $(document).ready(function () {
    $("#catalog_mobile_btn").click(function (e) {
      e.stopPropagation(), $(".catalog_mobile_main").toggleClass("active");
    }),
      $(document).click(function (e) {
        $(".catalog_mobile_main").is(e.target) ||
          0 !== $(".catalog_mobile_main").has(e.target).length ||
          $(".catalog_mobile_main").removeClass("active");
      });
  }),
  $(document).ready(function () {
    $(".catalog_mobile_item").click(function () {
      $(this).toggleClass("active");
    });
  }),
  $(document).ready(function () {
    var e = 0;
    $(".price_in_total").each(function () {
      e += parseInt($(this).text());
    }),
      $("#total_price").text(e + " ₽");
  }),
  $(document).ready(function () {
    $("#piggybank-form").submit(function (e) {
      e.preventDefault(),
        $.ajax({
          type: "POST",
          url: $(this).attr("action"),
          data: $(this).serialize(),
          success: function (e) {
            e.redirect && (window.location.href = e.redirect);
          },
          error: function (e, t, r) {
            var a = $("#error-container");
            a.empty(),
              e.responseJSON && e.responseJSON.error
                ? a.append(
                    '<p class="error-message">' + e.responseJSON.error + "</p>"
                  )
                : a.append(
                    '<p class="error-message">An error occurred. Please try again later.</p>'
                  );
          },
        });
    });
  });
