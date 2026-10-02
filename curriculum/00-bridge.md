# Bridge: the minimum systems toolkit

Use this bridge when a systems term interrupts your understanding of the course. The core starts with an infrastructure practitioner, not with an assumption that you already know machine learning. If you are also new to Linux, complete these exercises before month 1. This bridge is outside the 24 scheduled core months; repeat it until you can explain the result rather than reproduce a command.

**Prerequisites:** a terminal, a text editor, Python 3.11 or newer, and a copy of this repository. The authoring environment ran Python 3.11.11. Linux-specific observations require a Linux machine or an already available Linux VM. macOS can run all L0 Python labs but does not provide Linux `/proc`.

**You should finish able to:** follow a process from command to exit code; distinguish a file path from a running program; read a permission mode; separate name resolution from a connection; compare configuration revisions; explain what a container shares with its host; and calculate time, memory, power, and rates without mixing units. These are admission practice, not extra G1 assessments.

## A command starts a process

A program is stored instructions. A process is one execution of those instructions, with its own identity, memory, open files, and current directory. A terminal runs a shell, which interprets the command you type and starts another process. When you run `python3 labs/systems/lab.py list`, the shell locates the Python executable and passes two strings as arguments. Python opens the file and executes its code. The process eventually returns an exit status to the shell.

Three streams connect a command to its surroundings: standard input, standard output, and standard error. Output is the normal result; error is for diagnostics. An exit code of zero conventionally means success. This course deliberately uses code 1 for a failed simulated invariant, code 2 for an invalid command or environment, and code 3 for an intentional training interruption. Read both the status and the text. A long JSON output can describe failure.

On Linux, `/proc` exposes process and kernel information. `/proc/self/status` refers to the process reading it; fields such as `Pid`, `PPid`, and `VmRSS` describe that execution. Reading your own process information is enough for this exercise. Do not dump other processes' environment variables: they may contain secrets. This scope is documented in the [Linux proc filesystem guide](https://docs.kernel.org/filesystems/proc.html).

Try these from the repository root:

```bash
pwd
python3 --version
python3 -c 'import os; print("pid", os.getpid(), "parent", os.getppid(), "cwd", os.getcwd())'
python3 labs/systems/lab.py list
```

Predict which value will change when you repeat the third command. The current directory is inherited unless explicitly changed; the process identifier is allocated for each execution. Process IDs can later be reused, so a PID alone is not durable asset identity. On Linux, run `cat /proc/self/status` and explain why its PID describes `cat`, not the shell that launched it.

## Files, paths, and permissions

A directory maps names to filesystem objects. A relative path starts at the current directory; an absolute path starts at the filesystem root. Thus `learner-work/bridge/config.json` identifies different places if you launch the command from different directories. The course assumes its commands start at the repository root.

A file's contents, ownership, and permissions are different facts. Unix permission bits grant read, write, or execute permissions to its owner, group, and others. In a regular file, read means inspecting contents, write means changing contents, and execute means attempting to run it. For a directory, execute permits path traversal; it is not a request to run the directory. The digits encode bit sums: read is 4, write is 2, execute is 1. Therefore `640` means owner read/write, group read, others no permission. ACLs, elevated privilege, filesystem policy, and directory permissions can add constraints; the three digits alone do not prove an application's effective access. Python exposes the mode and permission bits through its [stat module](https://docs.python.org/3.11/library/stat.html).

Make a private practice directory and a harmless file using Python:

```bash
python3 - <<'PY'
from pathlib import Path
import stat
p = Path("learner-work/bridge")
p.mkdir(parents=True, exist_ok=True)
f = p / "config-before.json"
if f.exists():
    raise SystemExit("Practice file exists; inspect it before replacing anything")
f.write_text('{"replicas": 2}\n', encoding="ascii")
f.chmod(0o600)
print(f.resolve())
print(oct(stat.S_IMODE(f.stat().st_mode)))
PY
```

Expected: an absolute path ending in that filename and `0o600`. The leading `0o` says octal. This changes only your new practice file. Keep it for the Git exercise. Python's filesystem and permission interfaces are described in the [Python 3.11 OS reference](https://docs.python.org/3.11/library/os.html).

**Worked example: permission reasoning.** A checkpoint is owned by user `trainer`, has mode `600`, and the recovery process runs as `reader`. There is no applicable elevated privilege or ACL. The recovery process cannot read the file, even if the filename is correct and the disk is healthy. Changing a GPU driver cannot fix this. The next observation should be process identity and file/directory access, not device replacement. By contrast, a checksum mismatch after a successful read is evidence of a content/integrity problem; adding permissions would not repair those bytes.

## An address, a name, and a port solve different problems

An IP address identifies an interface in a network context. A hostname is a name that a resolver can map to one or more addresses. A port distinguishes transport endpoints at an address. The same server can listen for several services at different ports. A TCP connection additionally needs a reachable route and a listening endpoint. Resolving `trainer.example` does not prove that anything listens on its training rendezvous port. DNS supplies naming data; TCP supplies an ordered reliable byte stream between endpoints, with separate failure modes. See [DNS concepts, RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.html) and [TCP, RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html).

You can test the address/port distinction without contacting any remote host:

```bash
python3 - <<'PY'
import socket
with socket.socket() as server:
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    address = server.getsockname()
    with socket.create_connection(address, timeout=2) as client:
        connection, peer = server.accept()
        with connection:
            client.sendall(b"hello\n")
            print("server address:", address)
            print("received:", connection.recv(64).decode().strip())
PY
```

`127.0.0.1` is loopback: this traffic stays on your computer. Port zero asks the OS to select an available local port. Expect `received: hello`; the chosen port can vary. Closing the context managers closes the sockets. There is no lingering server. These interfaces are documented in [Python sockets](https://docs.python.org/3.11/library/socket.html).

Now reason about a counterexample: another machine cannot use *its* `127.0.0.1` to reach your server. Its loopback refers to itself. This exact conceptual error can appear when distributed workers receive a rendezvous address copied from a single-machine tutorial.

## Configuration is a proposal until you observe it taking effect

A configuration file records desired behavior. A running process may have loaded an earlier file, a different file, or an overridden value. Git can tell you how tracked text changed; it cannot prove what an already running process has loaded.

Create `learner-work/bridge/config-after.json` in your editor with `{"replicas": 3}`. Run:

```bash
git diff --no-index learner-work/bridge/config-before.json learner-work/bridge/config-after.json
```

Expect a removed line containing 2 and an added line containing 3. This comparison needs no Git commit. Exit code 1 is expected when the two files differ, as described by [Git's diff reference](https://git-scm.com/docs/git-diff). Write three separate statements: the file changed; the application reloaded; three replicas are serving. Only the first follows from this diff. You would need reload evidence and workload observations for the other two.

## Containers package an execution environment

An image packages filesystem content and execution metadata. A container is an execution of that image with runtime settings. Containers on a Linux host share the host kernel; they are not separate physical computers. CPU limits, mounted data, identities, networking, and exposed devices are runtime concerns. A GPU workload therefore depends on more than its image: the host driver and device exposure still matter. Docker explains this distinction in [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).

Do not install a container engine for this bridge. Instead, draw a process inside a box and place the kernel outside that box. Label four crossings: mounted files, network, identity, and GPU device access. Explain why a correctly built image can fail when launched without its data mount, and why changing its tag does not necessarily change an already running container. A digest identifies image content more precisely than a mutable tag, but correct content still needs correct runtime settings.

## Arithmetic is part of diagnosis

A bit is one binary digit; a byte contains eight bits. This course writes decimal gigabytes as GB (`10^9` bytes), binary gibibytes as GiB (`2^30` bytes), and gigabits per second as Gb/s. A rate has both a numerator and a denominator. If a checkpoint is measured in GB and a link in Gb/s, convert before dividing. Python uses `**` for exponentiation, `/` for division, and `//` for floor division; see the [Python introduction](https://docs.python.org/3.11/tutorial/introduction.html).

**Worked example: transfer time.** An 80 GB checkpoint crosses a link with a stated 40 Gb/s rate. First convert: `40 / 8 = 5 GB/s`. An ideal lower bound is `80 GB / 5 GB/s = 16 s`. If the measured end-to-end rate is 2 GB/s, use `80 / 2 = 40 s`. Protocol overhead, storage, shared traffic, and serialization mean the line rate is not an end-to-end promise. Writing `80 / 40 = 2 s` silently confuses bits and bytes.

**Worked example: memory.** A tensor has shape 2,048 by 4,096 and stores one four-byte value per element. Its payload is `2048 * 4096 * 4 = 33,554,432 bytes = 32 MiB`. Ten such tensors contain 320 MiB of payload. An application may allocate gradients, temporary results, and allocator bookkeeping as well. Payload is a lower-bound component, not total GPU memory consumption.

Practice these without looking at the key: 24 GiB in MiB; 3 kW sustained for 2 hours in kWh; 120 successful requests over 30 seconds in requests/s; and the time to read 12 GB at 3 GB/s. Record units at every line.

## Bridge checkpoint and answer key

Before proceeding, explain each answer aloud and reproduce both local scripts.

1. Why can a config diff and a serving replica count disagree?
2. Does a successful DNS lookup prove a TCP service is usable?
3. Does `600` mean that no process other than the owner can ever read a file?
4. Why does a containerized GPU program still depend on the host?
5. What are the four arithmetic answers above?

<details>
<summary>Answer key: read after your first attempt</summary>

1. The process may not have reloaded, may read another file, or may be unable to create the desired replicas. The diff proves text history, not observed state.
2. No. Naming, routing, transport connection, authentication, and application correctness are separate checks.
3. No. It describes ordinary mode bits; elevated privilege, ACLs, and other mechanisms require separate reasoning. Do not use a root-shell experiment to infer ordinary-user access.
4. The shared host kernel, host device driver, runtime device exposure, mounts, and limits remain dependencies.
5. 24,576 MiB; 6 kWh; 4 requests/s; 4 s. Units cancel in the rate calculations.

If you copied commands successfully but cannot explain these distinctions, repeat the relevant section. If Linux `/proc` was unavailable, record that observation as NOT_RUN, not a failed Linux host. Keep practice files rather than using a recursive delete command.

</details>

**Next:** [Month 1: map the system and bound failures](01-system-map.md).
