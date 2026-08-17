# AI-Powered IT Infrastructure Control System

---

## Overview

Have you ever wished you could simply ask your servers what's going on instead of memorizing endless command-line syntax? That's exactly what this project solves.

During my 5-week internship at Oil & Natural Gas Corporation (ONGC), I built a system that allows IT administrators to interact with their infrastructure through natural language. Instead of typing technical commands, you can ask questions like "Is the web server running?" and receive clear, human-readable answers.

The system combines artificial intelligence with workflow automation, vector databases for intelligent knowledge retrieval, and enterprise-grade security practices to make system administration more accessible and efficient.

---

## How It Works

### The Basic Flow

You type a question in plain English. The system interprets what you need, retrieves relevant context from its vector database knowledge base, runs the appropriate commands on your servers, and returns the results in a simple format. No SSH sessions, no command memorization, no accidental syntax errors.

### Behind the Scenes

An AI model powered by Mistral analyzes your request to understand the intent. The system then queries a Qdrant vector database to retrieve relevant historical context and past resolutions. The n8n automation engine selects the appropriate tool, executes the necessary system commands, captures the output, and formats it into a readable response. Everything gets logged for audit purposes with day-wise log files.

### What You Can Ask

The system handles routine administrative queries such as checking service status, verifying file sharing accessibility, monitoring disk space, confirming user access, and validating time synchronization across servers. It can also recall past incidents and their resolutions through semantic search capabilities.

---

## Key Features

### Natural Language Interface
You communicate with your infrastructure using everyday language. The system understands what you want without requiring specific command syntax. The Lovable AI frontend provides a user-friendly chat interface where you can submit natural language commands and receive meaningful responses.

### Vector Database and Semantic Search
Qdrant serves as the vector database for storing and retrieving embeddings of commands, logs, and resolutions. The system uses embedding models to convert text data into vector representations that capture semantic meaning. When you ask a question, the system performs semantic search to find relevant past incidents, making troubleshooting faster and more informed. This transforms unstructured operational data into searchable knowledge.

### Intelligent Command Execution
An AI agent using Mistral determines which system operations to perform based on your request. The agent operates with strict boundaries, responding only to predefined triggers related to IT administration tasks. It selects the right tool, executes the command, and processes the output. The agent can also reference past solutions stored in the vector database.

### Security-First Design
The system operates with restricted user accounts that have only the minimum permissions needed. All communication is encrypted using industry-standard protocols including SSH, HTTPS, and SFTP. The system follows the principle of least privilege, where users have exactly the permissions they need and nothing more.

### Comprehensive Logging and Auditing
Every command executed, every decision made, and every error encountered is logged in a centralized logging structure mounted from the host system. Day-wise log files are created for easy tracking. Command execution logs, error logs, and AI decisions are all captured. This provides a complete audit trail for troubleshooting and compliance purposes. Logs are also indexed in the vector database for future reference.

### Service Health Monitoring
The system can check the status of critical services including Nginx web servers, Samba file sharing services, vsftpd SFTP servers, and Chrony NTP time synchronization services. Automated health checks ensure services are running as expected.

### Context-Aware Assistance
By leveraging the Qdrant vector database, the system understands the context of your infrastructure, remembers past issues, and can suggest proven solutions based on historical data.

### Network Analysis
Wireshark captures and analyzes network traffic, helping verify that services are communicating correctly and troubleshooting connectivity issues. Packet capture during workflow execution provides visibility into SSH, SFTP, Samba, and NTP communication.

### Secure API Gateway
Ngrok securely exposes local services to the internet, creating an encrypted tunnel between the local system and ngrok cloud. This enables testing integrations with frontend interfaces and external services while maintaining data security.

---

## Technology Stack

### Infrastructure Layer
The system runs on Ubuntu Linux servers deployed as virtual machines using Oracle VirtualBox. This provides a safe, isolated environment for testing and operations. Two Ubuntu VMs were created to represent different server roles, with proper network configurations including NAT and Host-Only Adapter modes for secure communication.

### Containerization
Docker is used to deploy and manage the n8n automation engine, ensuring consistent behavior across different environments and simplifying updates. Volume mounting is implemented to store workflow data, logs, and configuration files persistently on the host system. Proper UID/GID mappings ensure containers have appropriate write access to mounted directories.

### Automation Engine
n8n serves as the workflow automation backbone. It coordinates the various components, executes system commands, and manages the flow of data between components. The engine acts as a bridge between the AI model and system-level operations, receiving structured input from the AI agent, executing validated commands, and returning only the required output fields.

### Artificial Intelligence
Mistral, a lightweight large language model deployed locally using Ollama, powers the natural language understanding capabilities. It interprets user requests and determines the appropriate actions. The AI agent is configured with strict system instructions to execute only real commands, never simulate results, and use only predefined tools. Running the model locally ensures data privacy and reduces dependency on external networks.

### Vector Database
Qdrant is used as the vector database for storing and retrieving embeddings of commands, logs, and resolutions. This enables semantic search capabilities, allowing the system to find similar past incidents and their solutions. The vector database transforms unstructured operational data into searchable knowledge, providing memory and context awareness to the system.

### Frontend Interface
Lovable AI serves as the frontend chat interface, providing a user-friendly way for users to submit natural language requests and receive processed outputs. It acts as the interaction layer, forwarding user requests to backend automation workflows and displaying responses in a clean, readable format.

### Communication Protocols
Secure Shell (SSH) enables encrypted communication between the host system and virtual machines. Key-based authentication replaces password-based access for enhanced security. SFTP via vsftpd provides secure file transfer operations with isolated user directories. Samba enables file sharing between Linux and Windows systems using the SMB/CIFS protocol.

### Time Synchronization
Chrony is configured as the NTP server to maintain consistent time across all servers. Accurate time synchronization is essential for log consistency, authentication, and automated workflows. Restricted sudo permissions allow specific users to execute time synchronization commands without full administrative rights.

### Web Server
Nginx serves as the high-performance web server for hosting web services and performing automated health checks. It is configured to respond to HTTP requests and monitored through n8n workflows to verify uptime and service availability.

### Network Analysis
Wireshark provides detailed visibility into data packets flowing across the network. Protocol-based and port-based filters isolate specific traffic such as SSH (port 22), HTTP/HTTPS (ports 80/443), SMB (port 445), and NTP (port 123), enabling quick identification of packet loss, misconfigurations, or blocked connections.

### Secure Tunneling
Ngrok creates encrypted tunnels between the local system and ngrok cloud, making it possible to access local servers from remote locations without complex network configuration. It also provides real-time request inspection and logging features for debugging webhook triggers.

---

## Vector Database Implementation

### What It Does
The Qdrant vector database serves as the system's memory and knowledge base. Every command executed, every error encountered, and every successful resolution is converted into vector embeddings and stored. When you ask a question, the system doesn't just execute commands—it first searches its memory for similar situations and their outcomes.

### How It Works
When a command is executed, the system uses embedding models to generate vector representations for the command, its output, and the context. These embeddings are stored in Qdrant along with metadata including timestamps, user information, and execution status. When a new query arrives, it's converted to an embedding and compared against stored vectors using cosine similarity. The most relevant past experiences are retrieved and presented to the AI agent for context.

### Benefits
- **Faster Troubleshooting:** Instead of starting from scratch, the system can reference how similar issues were resolved before.
- **Contextual Awareness:** The system understands the history of your infrastructure and learns from past interactions.
- **Intelligent Recommendations:** Based on historical data stored in vectors, the system can suggest solutions that worked previously.
- **Continuous Learning:** Every interaction improves the system's knowledge base, making it smarter over time.
- **Semantic Understanding:** The system finds relevant information even when exact wording doesn't match, thanks to semantic search capabilities.

### Technical Details
The vector database is integrated with n8n workflows through custom nodes that handle embedding generation and similarity search. Sentence transformers generate embeddings from text data. Vector search is performed using cosine similarity to find the most relevant matches. The system maintains indices for efficient retrieval as the knowledge base grows.

### Data Flow
1. User query is received and converted to vector embedding
2. Similarity search is performed against stored command embeddings
3. Relevant historical commands and their outputs are retrieved
4. AI agent uses this context to make informed decisions
5. New command execution and output are embedded and stored for future reference

---

## Security Implementation

Security was integrated into the system from the beginning rather than being added as an afterthought.

### Access Control
The system uses restricted user accounts that can only perform predefined operations. Users like 'terry' are created with limited privileges. Sudoers configuration allows only specific commands (such as chronyc for NTP operations) without granting full administrative privileges. SSH key-based authentication enhances security.

### Authentication
SSH key-based authentication replaces password-based access, providing stronger security. Restricted user permissions ensure that only authorized users can perform specific tasks. Sudoer configuration carefully controls what commands users can execute.

### Encryption
All communication between components uses encrypted protocols including SSH for remote access, HTTPS for web traffic, and SFTP for file transfers. SSH ensures encrypted communication between the host and virtual machines.

### Auditing
Comprehensive logging captures all system activities. Day-wise log files store command execution details, AI decisions, and system outputs. Every executed command, tool output, and AI decision is stored for auditing and troubleshooting purposes. This provides a complete record for security reviews and incident investigations.

### Network Security
Network segmentation is implemented through VLANs and managed switches. pfSense firewalls are configured to strengthen network security. IP-based access control ensures only authorized systems can communicate. In the project environment, proper network configuration with NAT and Host-Only adapters ensures secure communication between virtual machines.

### Data Privacy
Vector embeddings do not contain sensitive data in plain text. The system ensures that only authorized personnel can access stored logs and vector data through proper permission management.

### Principle of Least Privilege
Users and services get only the permissions they absolutely need. This fundamental security principle is applied throughout the system, from user account creation to command execution permissions.

---

## Services Configured and Managed

### SSH (OpenSSH)
Secure remote access to Ubuntu servers is enabled through SSH. Password-based authentication is replaced with key-based authentication to enhance security. User access restrictions ensure that only authorized users can perform specific tasks.

### SFTP (vsftpd)
The vsftpd server is configured to support SFTP-only access for specific users. User directories are isolated, and permissions are restricted to prevent unauthorized deletion or modification of files. This ensures secure file transfer while maintaining strict access control.

### Samba
Samba provides file sharing between Linux and Windows systems using the SMB/CIFS protocol. User-based access control regulates read and write permissions, while delete privileges are restricted. Cross-platform file sharing is enabled with proper permission management.

### NTP (Chrony)
Chrony is configured as the NTP server to maintain consistent time synchronization across all servers. Restricted sudo permissions allow specific users to execute time synchronization commands without granting full administrative rights. Accurate time sync is essential for log consistency and authentication.

### Nginx Web Server
Nginx serves as a high-performance web server for hosting web services and performing automated health checks. The server is configured to respond to HTTP requests and monitored through n8n workflows to verify uptime and service availability.

---

## Development Journey

### Starting Point: Self-Driven Learning
The project began with extensive self-driven learning to build a strong foundation in system administration and workflow automation. This phase focused on understanding Linux operating systems, server services, user permissions, and automation tools.

Key learning areas included:
- Linux file system hierarchy and permissions
- User and group management
- Secure remote access using SSH and SFTP
- Service monitoring and status verification
- Time synchronization using NTP
- Docker containerization concepts
- Workflow automation using n8n
- AI Agent-based decision making
- Vector databases and semantic search with Qdrant

Common Linux commands were practiced to understand real-world behavior, including whoami, df -h, ls, chmod, chown, systemctl, smbclient, and chronyc tracking.

### Planning and Installing Prerequisites
Before workflow development, proper planning and environment preparation were carried out. Ubuntu Linux virtual machines were used as target servers. The systems were updated using apt commands. Services including Docker, OpenSSH, SFTP, Samba, Chrony, and Nginx were installed and configured.

### User and Permission Management
Restricted users such as 'terry' were created using useradd and passwd commands. Permissions were carefully controlled using chmod and chown. Sudoer configuration allowed only specific commands (like chronyc) without granting full administrative privileges.

### Development of the Workflow Using AI Agent
The core implementation was done using n8n, where an AI Agent was used instead of traditional conditional logic (IF nodes). This allowed intelligent interpretation of user input and dynamic tool selection.

The workflow structure included:
- **Webhook Node:** Receives user requests from the frontend interface
- **AI Agent Node:** Serves as the decision engine using Mistral Chat Model with strict system messages defining the AI's role as an IT Administrator with limited permissions
- **Integrated Tool Nodes:** Dynamically selected and executed based on user intent including Machine Status Tool, Web Server Status Tool, FTP Status Tool, Samba Server Status Tool, and NTP Sync Check Tool

### Vector Database Integration
Qdrant vector database was integrated to add memory and context awareness. Custom nodes in n8n were implemented to handle embedding generation and vector storage. Commands and their outputs were indexed in Qdrant, enabling semantic search capabilities.

The embedding process involved:
1. Converting commands and outputs to vector embeddings
2. Storing embeddings in Qdrant with metadata
3. Performing similarity search for new queries
4. Retrieving relevant historical context for AI decision making

### Logging, File Handling, and Response Preparation
After tool execution, the workflow processes results through multiple stages:
- **Prepare Logs Node:** Structures command output, adds timestamps, and identifies command type and status
- **Read/Write Files from Disk Node:** Writes logs to a centralized directory ensuring auditability and traceability
- **Edit Fields Node:** Filters unnecessary technical details, extracts only relevant information, and formats output for user-friendly responses

This approach separates technical logging from user-facing responses, improving clarity and maintainability.

### Iterative Development and Testing
The project followed an iterative development approach. Each feature was:
- Tested manually via SSH
- Integrated into n8n as a tool
- Executed through the AI Agent
- Validated for correctness and permissions

Scenarios such as incorrect input, permission denial, service downtime, and command failure were tested. Workflow logic and system messages were refined based on testing outcomes and mentor feedback.

### Deployment
The final workflow was deployed using Docker containers to ensure portability and consistent runtime behavior. Deployment steps included running the n8n container, mounting persistent volumes for workflows and logs, and restarting containers without data loss.

Post-deployment verification confirmed:
- Webhook accessibility
- AI Agent decision accuracy
- Proper logging
- Secure execution of commands
- Vector database connectivity and search functionality

---

## Workflow Tools and Capabilities

### Machine Status Tool
Checks system health using commands such as whoami and df -h. Verifies user identity and disk usage.

### Web Server Status Tool
Monitors Nginx using systemctl status nginx. Checks containerized web services availability.

### FTP Status Tool
Validates SFTP operations using sftp user@host and directory listing commands like ls -la. Verifies file transfer accessibility and permissions.

### Samba Server Status Tool
Verifies Samba share accessibility using smbclient -L and smbclient //server/share. Validates cross-platform file sharing.

### NTP Sync Check Tool
Verifies time synchronization using chronyc tracking and chronyc sources. Ensures accurate system time across servers.

### AI Agent Configuration
The AI Agent is configured with strict system instructions:
- Respond only to simple user triggers
- Execute only real commands through tools
- Never simulate results or guess outputs
- Use only predefined tools
- Never mix tool responsibilities
- Run only once per user trigger

---

## Challenges Encountered and Solutions

### AI Interpretation Accuracy
Ensuring the AI model correctly interpreted user intent without executing unsafe commands required careful configuration and explicit system instructions in the system message. The AI was instructed to respond only to predefined triggers and never simulate results.

### Vector Database Integration
Configuring Qdrant for optimal performance required experimentation with different embedding models and similarity search parameters. Ensuring that embeddings accurately captured semantic meaning was an iterative process. Proper indexing was implemented to maintain search performance as the knowledge base grew.

### Security Constraints
Balancing automation capabilities with strict security controls was challenging. Restricting sudo access while still enabling required operations required thoughtful sudoers configuration. Only specific commands were allowed through restricted user accounts.

### Permission Management
File permission issues between the host system and Docker containers required resolution through proper volume mounting and user mapping. UID/GID mismatches were resolved to ensure containers had appropriate write access to mounted directories.

### Workflow Design Complexity
Designing workflows that could handle multiple command outputs and edge cases required careful planning and testing. The AI Agent approach simplified this compared to traditional conditional logic nodes.

### Debugging Automation Errors
Errors within automated workflows required detailed logging and analysis to identify root causes. Centralized logging with day-wise log files made troubleshooting significantly easier.

### Network Configuration
Getting virtual machines to communicate correctly required careful network configuration in VirtualBox. NAT and Host-Only adapters had to be configured properly for secure communication between VMs and the host system.

---

## What I Learned

### System Administration
The internship provided hands-on experience with Linux system administration, including user management, service configuration, and security best practices. I moved from basic command familiarity to genuine understanding of system operations. Working with SSH, SFTP, Samba, Chrony, and Nginx services gave me practical exposure to enterprise IT services.

### Vector Databases and Semantic Search
Working with Qdrant taught me the power of vector embeddings for knowledge retrieval. Understanding how semantic search works and implementing it for operational data was a significant learning experience. I learned how to convert unstructured operational data into searchable knowledge.

### Workflow Automation
n8n became a powerful tool for orchestrating complex IT operations. I learned how to design workflows with multiple nodes, handle variable command outputs, implement logging, and integrate AI decision-making. Replacing traditional IF logic with AI Agent provided flexibility and intelligence.

### AI Integration
Artificial intelligence is a powerful tool, but it requires careful implementation. The AI component works effectively because of the solid automation foundation beneath it. Running Mistral locally ensured data privacy and reduced external dependencies.

### Containerization
Docker enhanced my understanding of containerized environments, volume mounting, service persistence, and isolation. I learned how modern IT infrastructures rely heavily on containerization for scalability and easy deployment.

### Security First
Security cannot be added at the end of development. It must be part of the initial design, influencing decisions about access control, encryption, and logging from the beginning. SSH key-based authentication, restricted sudo access, and secure file permissions are essential practices.

### Networking
Exposure to network-level analysis tools such as Wireshark helped me understand how services communicate internally. Protocol-based analysis strengthened my knowledge of networking concepts, TCP/IP, encryption, and troubleshooting techniques.

### Iterative Development
Building something that works, testing it, learning from failures, and improving it proved more effective than trying to achieve perfection on the first attempt. Agile operational practices with regular updates and feedback-driven refinements were essential.

### Project Management
Clearly defining workflow objectives, command boundaries, and security constraints at the beginning made development more structured and reduced errors. Iterative development with continuous testing ensured early detection of failures.

---

## Results and Achievements

### Successful Implementation
The project successfully demonstrated an AI-assisted IT automation system capable of handling multiple administrative tasks through natural language interaction. The system went beyond basic configuration to build an intelligent, secure, and automated IT operations environment.

### AI Integration Achievement
A key achievement was the integration of AI Agent-based decision making within n8n workflows. Instead of relying on static conditional logic, the AI Agent dynamically interpreted user intent and selected appropriate workflow paths, making the system flexible and scalable.

### Automation Success
Core system administration operations were successfully automated including:
- Service health checks (Nginx, Docker, Chrony)
- Secure remote access through SSH
- File operations via SFTP and Samba
- Time synchronization validation
- System monitoring and command execution

### Vector Database Enhancement
The Qdrant integration added memory and context awareness to the system, enabling intelligent knowledge retrieval and continuous learning from past interactions.

### User Interaction Improvement
Through the Lovable AI interface, users could submit requests in natural language instead of executing complex command-line operations. The system responded with concise, filtered outputs while maintaining detailed logs internally. This improved usability and reduced human error.

### Operational Efficiency
The system demonstrated faster execution of repetitive administrative tasks, standardized responses across operations, and reduced dependency on direct server access for routine checks.

### Technical Reliability
The system performed reliably across different services and workflows. n8n workflows executed commands consistently, service monitoring ensured expected operations, Docker deployment provided isolation and stability, and secure protocols ensured encrypted communication.

### Security Validation
Restricted user access with limited sudo privileges, SSH key-based authentication, secure file permissions, and controlled service exposure followed enterprise security standards. Centralized logging ensured traceability and accountability.

---

## Future Scope

### Advanced Monitoring Dashboards
Future improvements can include visual dashboards displaying real-time server health metrics such as CPU usage, memory utilization, disk space, and network latency. These would provide administrators with instant insights and improve visibility.

### Alerting and Notification System
Integration with email, Slack, or SMS services can enable automated alerts when system thresholds are breached, such as service downtime, failed SSH attempts, or NTP synchronization issues. This would enable proactive incident response.

### Expanded AI Decision-Making
The AI Agent can be enhanced to perform predictive analysis, recommend corrective actions, and automatically resolve common system issues based on historical logs and patterns stored in the vector database.

### Enhanced Vector Search
Implementing hybrid search combining semantic and keyword search would provide more accurate retrieval of relevant information from the vector database.

### Security Enhancements
Additional security layers such as IP whitelisting, multi-factor authentication for critical workflows, and anomaly detection can be incorporated to further protect the infrastructure. Integration with pfSense firewalls for advanced network security.

### Cross-Platform Support
The workflow can be extended to manage Windows servers and cloud-based instances (AWS, Azure, GCP), making it a unified automation platform for hybrid environments.

### Network Analysis Integration
Deeper integration with tools like Wireshark can allow automated packet capture and traffic analysis during network troubleshooting scenarios, with results stored in the vector database for future reference.

### Scalability with Containerization
Containerizing the n8n setup using Docker and Kubernetes can improve scalability, fault tolerance, and deployment flexibility in enterprise environments.

### Continuous Learning Pipeline
Implementing automated processes to update embeddings and refine search capabilities as new data becomes available, ensuring the system continuously improves.

### Self-Healing Capabilities
Enabling the system to automatically resolve common issues based on historical resolutions stored in the vector database would further reduce manual intervention and improve system reliability.

### Digital Forensics Integration
Leveraging cybersecurity expertise to add forensic analysis capabilities, enabling the system to detect and respond to security incidents.

---

nts require.
