document.querySelectorAll('.clickable-row').forEach(row => {
    // Her satıra hover (fare üstüne gelme) olayını ekleyelim
    row.style.cursor = 'pointer';  // Satıra pointer imlecini ekliyoruz
  
    row.addEventListener("click", function() {
      const dokumanId = row.id.split('-')[1]; 
      window.location.href = `/dokuman-goruntule/${dokumanId}/`;
    });
  });
  