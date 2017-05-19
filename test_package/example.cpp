#include <iostream>

#include <GLFW/glfw3.h>

int main(void)
{
	GLFWwindow* window = NULL;

	if (glfwInit())
	{
		std::cout << "glfwInit() test succesful." << std::endl;
		glfwTerminate();
	}
	else
	{
		std::cout << "glfwInit() failed during test." << std::endl;
	}
}

