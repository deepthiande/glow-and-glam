/**
 * GLOW & GLAM - Luxury Cosmetics Frontend Interactions
 * Vanilla JavaScript (No React / Framework dependencies)
 */

document.addEventListener('DOMContentLoaded', () => {
  initStickyHeader();
  initMobileNav();
  initSearchAutocomplete();
  initQuickViewModal();
  initAjaxCart();
  initAjaxWishlist();
  initProductGallery();
  initShadeSelectors();
  initProductTabs();
  initCartQuantityUpdaters();
  initToastAutoDismiss();
});

/* Helper: Get CSRF Token from cookie */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/* 1. Sticky Navigation Header Effect */
function initStickyHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

/* 2. Mobile Navigation Toggle */
function initMobileNav() {
  const toggleBtn = document.querySelector('.mobile-toggle-btn');
  const mobileMenu = document.querySelector('.mobile-menu-drawer');
  const closeBtn = document.querySelector('.mobile-menu-close');

  if (toggleBtn && mobileMenu) {
    toggleBtn.addEventListener('click', () => {
      mobileMenu.classList.add('active');
      document.body.style.overflow = 'hidden';
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
      });
    }

    mobileMenu.addEventListener('click', (e) => {
      if (e.target === mobileMenu) {
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }
}

/* 3. Search Autocomplete & Toggle */
function initSearchAutocomplete() {
  const searchToggleBtn = document.querySelector('.search-toggle-btn');
  const searchDropdown = document.querySelector('.search-bar-dropdown');
  const searchInput = document.querySelector('.search-input');
  const suggestionsBox = document.querySelector('.search-suggestions-box');

  if (searchToggleBtn && searchDropdown) {
    searchToggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      searchDropdown.classList.toggle('active');
      if (searchDropdown.classList.contains('active') && searchInput) {
        searchInput.focus();
      }
    });
  }

  if (searchInput && suggestionsBox) {
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      const query = e.target.value.trim();

      if (query.length < 2) {
        suggestionsBox.innerHTML = '';
        suggestionsBox.style.display = 'none';
        return;
      }

      debounceTimer = setTimeout(() => {
        fetch(`/api/search/?q=${encodeURIComponent(query)}`)
          .then(res => res.json())
          .then(data => {
            if (data.results && data.results.length > 0) {
              suggestionsBox.innerHTML = data.results.map(item => `
                <a href="${item.url}" class="search-suggestion-item">
                  <img src="${item.image}" alt="${item.title}" class="search-suggestion-thumb" />
                  <div>
                    <div style="font-weight:600; font-size:0.9rem; color:var(--color-text-main);">${item.title}</div>
                    <div style="font-size:0.78rem; color:var(--color-primary);">${item.category} • ${item.price}</div>
                  </div>
                </a>
              `).join('');
              suggestionsBox.style.display = 'block';
            } else {
              suggestionsBox.innerHTML = '<div style="padding:1rem; text-align:center; color:var(--color-text-muted); font-size:0.88rem;">No products found for this search.</div>';
              suggestionsBox.style.display = 'block';
            }
          })
          .catch(err => console.error('Search autocomplete error:', err));
      }, 250);
    });

    // Close suggestion box on outside click
    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.style.display = 'none';
      }
    });
  }
}

/* 4. Quick View Modal */
function initQuickViewModal() {
  const modal = document.getElementById('quickViewModal');
  if (!modal) return;

  const closeBtn = modal.querySelector('.modal-close-btn');
  const modalBody = modal.querySelector('.modal-body-content');

  // Open modal on click
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.quick-view-btn');
    if (!btn) return;

    e.preventDefault();
    const productId = btn.dataset.productId;
    if (!productId) return;

    modalBody.innerHTML = `
      <div style="text-align:center; padding: 4rem 2rem;">
        <i class="fa-solid fa-spinner fa-spin" style="font-size:2rem; color:var(--color-primary);"></i>
        <p style="margin-top:1rem; color:var(--color-text-muted);">Loading luxury product details...</p>
      </div>
    `;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    fetch(`/api/quick-view/${productId}/`)
      .then(res => res.json())
      .then(product => {
        let swatchesHtml = '';
        if (product.shades && product.shades.length > 0) {
          swatchesHtml = `
            <div style="margin-bottom:1.5rem;">
              <div style="font-size:0.85rem; font-weight:600; margin-bottom:0.5rem;">
                Select Shade: <span class="modal-selected-shade" style="color:var(--color-primary);">${product.shades[0].name}</span>
              </div>
              <div class="shade-swatches-grid modal-shades">
                ${product.shades.map((s, idx) => `
                  <div class="shade-swatch-item ${idx === 0 ? 'active' : ''}" 
                       data-shade-id="${s.id}" 
                       data-shade-name="${s.name}" 
                       style="background-color: ${s.color_hex};" 
                       title="${s.name}"></div>
                `).join('')}
              </div>
            </div>
          `;
        }

        modalBody.innerHTML = `
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; padding: 2.5rem;">
            <div>
              <div style="width:100%; height:380px; border-radius:var(--radius-md); overflow:hidden; background:var(--color-bg-warm); margin-bottom:1rem;">
                <img id="modalMainImg" src="${product.images[0]}" alt="${product.title}" style="width:100%; height:100%; object-fit:cover;" />
              </div>
              <div style="display:flex; gap:0.5rem; overflow-x:auto;">
                ${product.images.map(img => `
                  <button type="button" class="gallery-thumb-btn modal-thumb" onclick="document.getElementById('modalMainImg').src='${img}'" style="width:60px; height:60px; border-radius:var(--radius-sm); overflow:hidden;">
                    <img src="${img}" style="width:100%; height:100%; object-fit:cover;" />
                  </button>
                `).join('')}
              </div>
            </div>
            <div>
              <div style="font-size:0.78rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--color-accent); font-weight:700; margin-bottom:0.35rem;">
                ${product.brand}
              </div>
              <h2 style="font-size:1.8rem; margin-bottom:0.65rem;">${product.title}</h2>
              <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem; color:var(--color-gold); font-size:0.88rem;">
                <i class="fa-solid fa-star"></i>
                <span style="font-weight:600; color:var(--color-text-main);">${product.rating}</span>
                <span style="color:var(--color-text-muted);">(${product.review_count} reviews)</span>
              </div>
              <div style="display:flex; align-items:baseline; gap:0.75rem; margin-bottom:1.25rem;">
                <span style="font-size:1.6rem; font-weight:700; color:var(--color-text-main);">${product.price}</span>
                ${product.original_price ? `<span style="font-size:1.1rem; color:var(--color-text-light); text-decoration:line-through;">${product.original_price}</span>` : ''}
                ${product.discount_percent ? `<span class="badge badge-discount">-${product.discount_percent}%</span>` : ''}
              </div>
              <p style="font-size:0.92rem; color:var(--color-text-muted); line-height:1.6; margin-bottom:1.5rem;">
                ${product.short_description}
              </p>
              
              <form action="/cart/add/" method="POST" class="ajax-add-cart-form">
                <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken') || ''}" />
                <input type="hidden" name="product_id" value="${product.id}" />
                <input type="hidden" name="shade_id" id="modalShadeInput" value="${product.shades && product.shades.length ? product.shades[0].id : ''}" />

                ${swatchesHtml}

                <div style="display:flex; gap:1rem; margin-bottom:1.5rem;">
                  <div class="qty-stepper">
                    <button type="button" class="qty-btn" onclick="let input=this.nextElementSibling; if(input.value>1) input.value--;">-</button>
                    <input type="number" name="quantity" value="1" min="1" class="qty-input" />
                    <button type="button" class="qty-btn" onclick="let input=this.previousElementSibling; input.value++;">+</button>
                  </div>
                  <button type="submit" class="btn btn-primary" style="flex-grow:1;">
                    <i class="fa-solid fa-bag-shopping"></i> Add to Luxury Bag
                  </button>
                </div>
              </form>

              <div style="margin-top:1rem; padding-top:1rem; border-top:1px solid var(--color-border); font-size:0.85rem; color:var(--color-text-muted);">
                <a href="${product.url}" style="color:var(--color-primary); font-weight:600;">View Full Product Specifications & Customer Reviews &rarr;</a>
              </div>
            </div>
          </div>
        `;

        // Bind swatches in modal
        const modalShades = modalBody.querySelectorAll('.modal-shades .shade-swatch-item');
        const modalShadeLabel = modalBody.querySelector('.modal-selected-shade');
        const modalShadeInput = modalBody.querySelector('#modalShadeInput');

        modalShades.forEach(swatch => {
          swatch.addEventListener('click', () => {
            modalShades.forEach(s => s.classList.remove('active'));
            swatch.classList.add('active');
            if (modalShadeLabel) modalShadeLabel.textContent = swatch.dataset.shadeName;
            if (modalShadeInput) modalShadeInput.value = swatch.dataset.shadeId;
          });
        });
      })
      .catch(err => {
        modalBody.innerHTML = '<div style="padding:3rem; text-align:center; color:red;">Failed to load product details.</div>';
      });
  });

  // Close handlers
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modal.classList.remove('active');
      document.body.style.overflow = '';
    });
  }
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
}

/* 5. AJAX Add to Cart */
function initAjaxCart() {
  document.addEventListener('submit', (e) => {
    const form = e.target.closest('.ajax-add-cart-form');
    if (!form) return;

    e.preventDefault();
    const formData = new FormData(form);

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';
    if (submitBtn) {
      submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';
      submitBtn.disabled = true;
    }

    fetch('/cart/add/', {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: formData,
    })
      .then(res => res.json())
      .then(data => {
        if (submitBtn) {
          submitBtn.innerHTML = originalBtnHtml;
          submitBtn.disabled = false;
        }

        if (data.status === 'success') {
          // Update cart badge counts
          document.querySelectorAll('.nav-cart-count').forEach(badge => {
            badge.textContent = data.cart_items_count;
            badge.style.display = data.cart_items_count > 0 ? 'flex' : 'none';
          });

          showToast(data.message || '✨ Added to your shopping bag!', 'success');

          // If inside quick view modal, close modal
          const modal = document.getElementById('quickViewModal');
          if (modal && modal.classList.contains('active')) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
          }
        } else {
          showToast('Could not add to cart. Please try again.', 'error');
        }
      })
      .catch(err => {
        if (submitBtn) {
          submitBtn.innerHTML = originalBtnHtml;
          submitBtn.disabled = false;
        }
        form.submit(); // fallback to standard submit
      });
  });
}

/* 6. AJAX Wishlist Toggle */
function initAjaxWishlist() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.ajax-wishlist-toggle');
    if (!btn) return;

    e.preventDefault();
    const productId = btn.dataset.productId;
    if (!productId) return;

    fetch(`/wishlist/toggle/${productId}/`, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          // Update all wishlist buttons for this product
          document.querySelectorAll(`.ajax-wishlist-toggle[data-product-id="${productId}"]`).forEach(b => {
            const icon = b.querySelector('i');
            if (data.action === 'added') {
              b.classList.add('active-wishlist');
              if (icon) {
                icon.classList.remove('fa-regular');
                icon.classList.add('fa-solid');
              }
            } else {
              b.classList.remove('active-wishlist');
              if (icon) {
                icon.classList.remove('fa-solid');
                icon.classList.add('fa-regular');
              }
            }
          });

          // Update navbar wishlist count
          document.querySelectorAll('.nav-wishlist-count').forEach(badge => {
            badge.textContent = data.wishlist_count;
            badge.style.display = data.wishlist_count > 0 ? 'flex' : 'none';
          });

          showToast(data.message, data.action === 'added' ? 'success' : 'info');
        }
      })
      .catch(err => console.error('Wishlist error:', err));
  });
}

/* 7. Product Detail Image Gallery */
function initProductGallery() {
  const mainImage = document.getElementById('mainDetailImage');
  const thumbs = document.querySelectorAll('.detail-gallery-thumb');

  if (mainImage && thumbs.length > 0) {
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        thumbs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        const newSrc = thumb.dataset.largeSrc || thumb.querySelector('img').src;
        mainImage.style.opacity = '0.4';
        setTimeout(() => {
          mainImage.src = newSrc;
          mainImage.style.opacity = '1';
        }, 150);
      });
    });
  }
}

/* 8. Shade Selectors */
function initShadeSelectors() {
  const swatchContainers = document.querySelectorAll('.product-shades-selector');
  swatchContainers.forEach(container => {
    const swatches = container.querySelectorAll('.shade-swatch-item');
    const label = container.querySelector('.selected-shade-name');
    const input = container.querySelector('input[name="shade_id"]');

    swatches.forEach(swatch => {
      swatch.addEventListener('click', () => {
        swatches.forEach(s => s.classList.remove('active'));
        swatch.classList.add('active');
        if (label) label.textContent = swatch.dataset.shadeName;
        if (input) input.value = swatch.dataset.shadeId;
      });
    });
  });
}

/* 9. Product Details Tabs */
function initProductTabs() {
  const tabs = document.querySelectorAll('.tab-nav-btn');
  const panels = document.querySelectorAll('.tab-content-panel');

  if (tabs.length && panels.length) {
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetId = tab.dataset.tabTarget;
        tabs.forEach(t => t.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));

        tab.classList.add('active');
        const targetPanel = document.getElementById(targetId);
        if (targetPanel) targetPanel.classList.add('active');
      });
    });
  }
}

/* 10. Cart Quantity AJAX Updaters */
function initCartQuantityUpdaters() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.cart-qty-action-btn');
    if (!btn) return;

    e.preventDefault();
    const itemId = btn.dataset.itemId;
    const action = btn.dataset.action; // 'increase' or 'decrease'
    if (!itemId) return;

    const row = document.getElementById(`cartItemRow-${itemId}`);

    fetch(`/cart/update/${itemId}/`, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `action=${encodeURIComponent(action)}`
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          if (!data.item_exists && row) {
            row.remove();
          } else if (row) {
            const qtyInput = row.querySelector('.cart-item-qty-input');
            const itemTotal = row.querySelector('.cart-item-total-price');
            if (qtyInput) qtyInput.value = data.item_quantity;
            if (itemTotal) itemTotal.textContent = data.item_total;
          }

          // Update summary
          updateCartSummaryUi(data);

          if (data.cart_items_count === 0) {
            window.location.reload();
          }
        }
      })
      .catch(err => console.error('Cart quantity update error:', err));
  });
}

function updateCartSummaryUi(data) {
  // Update badges
  document.querySelectorAll('.nav-cart-count').forEach(badge => {
    badge.textContent = data.cart_items_count;
  });

  const subtotalEl = document.getElementById('summarySubtotal');
  const discountEl = document.getElementById('summaryDiscount');
  const shippingEl = document.getElementById('summaryShipping');
  const taxEl = document.getElementById('summaryTax');
  const grandTotalEl = document.getElementById('summaryGrandTotal');

  if (subtotalEl) subtotalEl.textContent = data.subtotal;
  if (discountEl) discountEl.textContent = data.discount;
  if (shippingEl) shippingEl.textContent = data.shipping;
  if (taxEl) taxEl.textContent = data.tax;
  if (grandTotalEl) grandTotalEl.textContent = data.grand_total;
}

/* 11. Toast Notifications */
function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast-message toast-${type}`;
  const icon = type === 'success' ? 'fa-circle-check' : (type === 'error' ? 'fa-circle-exclamation' : 'fa-circle-info');
  toast.innerHTML = `
    <i class="fa-solid ${icon}" style="font-size:1.2rem; color:var(--color-${type === 'success' ? 'primary' : (type === 'error' ? 'red' : 'primary')});"></i>
    <div style="flex-grow:1;">${message}</div>
    <button type="button" style="color:var(--color-text-light); font-size:1rem;" onclick="this.parentElement.remove()">&times;</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.35s ease';
    setTimeout(() => toast.remove(), 350);
  }, 4500);
}

function initToastAutoDismiss() {
  document.querySelectorAll('.toast-message').forEach(toast => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.35s ease';
      setTimeout(() => toast.remove(), 350);
    }, 4500);
  });
}
