document.addEventListener("DOMContentLoaded", () => {
  const textForm = document.getElementById("textForm");
  const predictedTopicElement = document.getElementById("predictedTopic");
  const probabilitiesListElement = document.getElementById("probabilitiesList");
  const submitButton = textForm.querySelector("button[type='submit']");

  // Add animation to the form elements
  animateFormElements();

  // Add ripple effect to the submit button
  addRippleEffect(submitButton);

  textForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Form validation
    if (!validateForm()) {
      return;
    }

    // Show loading state with animation
    submitButton.disabled = true;
    submitButton.innerHTML =
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Đang xử lý...';

    predictedTopicElement.innerHTML =
      '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    probabilitiesListElement.innerHTML =
      '<div class="text-center py-3"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';

    // Get form data
    const formData = new FormData(textForm);

    try {
      // Send data to server with a small artificial delay to show the loading state
      await new Promise((resolve) => setTimeout(resolve, 800)); // Simulated delay for UX

      const response = await fetch("/classify", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      // Display predicted topic with fade-in animation
      fadeIn(predictedTopicElement, data.predicted_topic);

      // Display probabilities with animation
      displayProbabilities(data.probabilities);
    } catch (error) {
      console.error("Error:", error);

      fadeIn(
        predictedTopicElement,
        '<span class="text-danger">Đã xảy ra lỗi khi phân loại</span>'
      );

      probabilitiesListElement.innerHTML =
        '<div class="alert alert-danger">Đã xảy ra lỗi khi xử lý yêu cầu. Vui lòng thử lại sau.</div>';
    } finally {
      // Reset button state
      submitButton.disabled = false;
      submitButton.textContent = "Phân loại";
    }
  });

  // Function to validate form
  function validateForm() {
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const content = document.getElementById("content").value.trim();

    let isValid = true;

    if (!title) {
      showError("title", "Vui lòng nhập tiêu đề");
      isValid = false;
    } else {
      clearError("title");
    }

    if (!description) {
      showError("description", "Vui lòng nhập mô tả");
      isValid = false;
    } else {
      clearError("description");
    }

    if (!content) {
      showError("content", "Vui lòng nhập nội dung");
      isValid = false;
    } else {
      clearError("content");
    }

    return isValid;
  }

  // Function to show validation error
  function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    field.classList.add("is-invalid");

    // Check if error message already exists
    let errorDiv = field.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains("invalid-feedback")) {
      errorDiv = document.createElement("div");
      errorDiv.className = "invalid-feedback";
      field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    errorDiv.textContent = message;
  }

  // Function to clear validation error
  function clearError(fieldId) {
    const field = document.getElementById(fieldId);
    field.classList.remove("is-invalid");

    const errorDiv = field.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains("invalid-feedback")) {
      errorDiv.textContent = "";
    }
  }

  // Add event listeners for real-time validation
  document
    .getElementById("title")
    .addEventListener("input", () => clearError("title"));
  document
    .getElementById("description")
    .addEventListener("input", () => clearError("description"));
  document
    .getElementById("content")
    .addEventListener("input", () => clearError("content"));

  // Function to display probabilities with animation
  function displayProbabilities(probabilities) {
    // Clear previous content
    probabilitiesListElement.innerHTML = "";

    // Sort probabilities in descending order
    probabilities.sort((a, b) => b.probability - a.probability);

    // Create and append elements with staggered animations
    probabilities.forEach((item, index) => {
      const probabilityPercentage = (item.probability * 100).toFixed(2);

      // Choose icon based on topic category
      const icon = getTopicIcon(item.topic);

      const topicItem = document.createElement("div");
      topicItem.className = "topic-item";
      topicItem.style.opacity = "0";
      topicItem.style.transform = "translateY(10px)";

      // Add a slight color variation based on probability
      const colorIntensity = Math.max(
        20,
        Math.min(90, Math.floor(item.probability * 100))
      );
      const borderColor = index < 3 ? getTopColor(index) : `#3498db`;

      topicItem.innerHTML = `
          <div class="topic-details">
              <div class="topic-name"><i class="${icon} me-2"></i>${item.topic}</div>
              <div class="probability-bar">
                  <div class="probability-value" style="width: 0%; background: ${borderColor};"></div>
              </div>
          </div>
          <div class="topic-probability" style="background-color: rgba(52, 152, 219, 0.${colorIntensity});">0.00%</div>
      `;

      probabilitiesListElement.appendChild(topicItem);

      // Animate each item with a staggered delay
      setTimeout(() => {
        topicItem.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        topicItem.style.opacity = "1";
        topicItem.style.transform = "translateY(0)";

        // Animate the probability value
        const probabilityBar = topicItem.querySelector(".probability-value");
        const probabilityValueElement =
          topicItem.querySelector(".topic-probability");

        setTimeout(() => {
          probabilityBar.style.transition = "width 1s ease-in-out";
          probabilityBar.style.width = `${probabilityPercentage}%`;

          // Animate the percentage text
          animateCounter(
            probabilityValueElement,
            0,
            probabilityPercentage,
            800
          );
        }, 300);
      }, 50 * index);
    });
  }

  // Function to get a suitable icon for a topic
  function getTopicIcon(topic) {
    const topicLower = topic.toLowerCase();

    // Map topics to appropriate Font Awesome icons
    if (topicLower.includes("quỹ") || topicLower.includes("vọng"))
      return "fas fa-hand-holding-heart";
    if (topicLower.includes("gia đình") || topicLower.includes("tổ ấm"))
      return "fas fa-home";
    if (topicLower.includes("hồ sơ") || topicLower.includes("phá án"))
      return "fas fa-search";
    if (topicLower.includes("giải trí") || topicLower.includes("sao"))
      return "fas fa-star";
    if (topicLower.includes("dân sinh")) return "fas fa-users";
    if (topicLower.includes("sức khoẻ")) return "fas fa-heartbeat";
    if (topicLower.includes("nhạc")) return "fas fa-music";
    if (topicLower.includes("nhịp sống")) return "fas fa-coffee";
    if (topicLower.includes("phim")) return "fas fa-film";
    if (topicLower.includes("sân khấu") || topicLower.includes("mỹ thuật"))
      return "fas fa-theater-masks";
    if (topicLower.includes("người việt") || topicLower.includes("5 châu"))
      return "fas fa-globe-asia";
    if (topicLower.includes("thể thao")) return "fas fa-futbol";
    if (topicLower.includes("giáo dục") || topicLower.includes("học"))
      return "fas fa-graduation-cap";
    if (topicLower.includes("quân sự")) return "fas fa-shield-alt";
    if (
      topicLower.includes("kinh doanh") ||
      topicLower.includes("doanh nghiệp")
    )
      return "fas fa-briefcase";
    if (topicLower.includes("ai")) return "fas fa-robot";
    if (topicLower.includes("chứng khoán")) return "fas fa-chart-line";
    if (topicLower.includes("thị trường") || topicLower.includes("xe"))
      return "fas fa-car";
    if (topicLower.includes("vũ trụ")) return "fas fa-space-shuttle";
    if (topicLower.includes("ẩm thực")) return "fas fa-utensils";

    // Default icon for unmatched topics
    return "fas fa-bookmark";
  }

  // Function to get color for top topics
  function getTopColor(index) {
    const colors = [
      "linear-gradient(90deg, #f1c40f, #e74c3c)", // 1st place - gold/red
      "linear-gradient(90deg, #3498db, #2980b9)", // 2nd place - blue
      "linear-gradient(90deg, #2ecc71, #27ae60)", // 3rd place - green
    ];

    return colors[index] || "linear-gradient(90deg, #3498db, #2980b9)";
  }

  // Function to animate a counter from start to end
  function animateCounter(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const value = progress * (end - start) + start;
      element.textContent = `${value.toFixed(2)}%`;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  }

  // Function to fade in an element with text
  function fadeIn(element, content) {
    element.style.opacity = "0";

    // If content is just text (not HTML), wrap it in a centered structure
    if (!content.includes("<")) {
      element.innerHTML = `<div class="text-center w-100">${content}</div>`;
    } else {
      element.innerHTML = content;
    }

    setTimeout(() => {
      element.style.transition = "opacity 0.5s ease";
      element.style.opacity = "1";
    }, 100);
  }

  // Function to add ripple effect to buttons
  function addRippleEffect(button) {
    button.addEventListener("click", function (e) {
      const rect = button.getBoundingClientRect();

      const circle = document.createElement("span");
      const diameter = Math.max(button.clientWidth, button.clientHeight);
      const radius = diameter / 2;

      circle.style.width = circle.style.height = `${diameter}px`;
      circle.style.left = `${e.clientX - rect.left - radius}px`;
      circle.style.top = `${e.clientY - rect.top - radius}px`;
      circle.classList.add("ripple");

      const ripple = button.getElementsByClassName("ripple")[0];
      if (ripple) {
        ripple.remove();
      }

      button.appendChild(circle);
    });
  }

  // Function to add initial animation to form elements
  function animateFormElements() {
    const formElements = textForm.querySelectorAll(".form-control, .btn");

    formElements.forEach((element, index) => {
      element.style.opacity = "0";
      element.style.transform = "translateY(20px)";

      setTimeout(() => {
        element.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        element.style.opacity = "1";
        element.style.transform = "translateY(0)";
      }, 100 + index * 100);
    });
  }
});
